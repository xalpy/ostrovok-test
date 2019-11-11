#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Nikita Markozov"

import re
import sys
import urllib.request
import os

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Parser:
    def __init__(self, month: str, year: int) -> None:
        """
        Программа занимается скачиванием фонов с сайта smashingmagazine во всех доступных форматах
        """
        self.logger = logging.getLogger(self.__module__)
        self.month = month.lower()
        self.year = year
        self.month_code: str = ""
        self.url = "https://www.smashingmagazine.com/"
        self.months_choices = {'january': '00', 'february': '01', 'march': '02',
                               'april': '03', 'may': '04', 'june': '05',
                               'jule': '06', 'august': '07', 'september': '08',
                               'october': '09', 'november': '10', 'december': '11'}

    def get_month_and_year(self) -> None:
        """
        Проверяет есть ли вводимый в аргументы программы месяц, в списке разрешенных.
        """
        for i in self.months_choices:
            if self.month == i:
                return None

    def get_page(self) -> str:
        """
        Загружает страницу по нужному месяцу и году
        """
        self.get_month_and_year()
        for i in self.months_choices:
            if i == self.month:
                self.month_code = self.months_choices[i]
                break
        url = f'{self.url}{self.year}/{self.month_code}/desktop-wallpaper-calendars-{self.month}-{self.year}'
        page = requests.get(url).text
        return page

    @staticmethod
    def download_pic(list_: list) -> bool:
        """
        Загружает картинки в каталог pictures из списка ссылок на картинки
        """
        if not os.path.isdir("./pictures"):
            os.mkdir("./pictures")
        for i in tqdm(list_):
            try:
                img = urllib.request.urlopen(i).read()
                with open('pictures/' + i.split('/')[-1], 'wb') as file:
                    file.write(img)
            except TypeError as e:
                return False
        return True

    def parse_picture(self) -> None:
        """
        Вытаскивает ссылки на картинки со страницы
        """
        page = self.get_page()
        soup = bs(page, 'lxml')
        urls_ = soup.find_all('a', href=True)

        pictures_url = []
        for i in urls_:
            try:
                url = i.get('href')
                if re.search('jpg|png', url):
                    pictures_url.append(url)
            except TypeError as e:
                logger.error(e)
        if self.download_pic(pictures_url):
            self.logger.info('success')
        else:
            self.logger.info('denied')


if __name__ == '__main__':
    try:
        a = Parser(sys.argv[1], int(sys.argv[2]))
        a.parse_picture()
    except ValueError:
        logger.error("Один из параметров не верный")
    except IndexError:
        logger.error('Введите параметры: месяц(may, june) и год(2017, 2018)')
