import requests

from bs4 import BeautifulSoup as bs

import urllib.request

import re

import datetime

import sys


class Parser:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.months_choices ={'january': '00', 'february': '01', 'march': '02',
                              'april': '03', 'may': '04', 'june': '05',
                              'jule': '06', 'august': '07', 'september': '08',
                              'october': '09', 'november': '10','december':'11'}


    def get_month_and_year(self):

        for i in self.months_choices:
            if self.month.lower() == i:
                return
        print('месяц или год не соответсвуют стандарту:\n\
пример(месяц): may, june, october\n\
пример(год): 2010, 2017')


    def get_page(self):
        self.get_month_and_year()
        for i in self.months_choices:
            if i == self.month.lower():
                self.month_code = self.months_choices[i]
                break

        url = f'https://www.smashingmagazine.com/{self.year}/{self.month_code}\
/desktop-wallpaper-calendars-{self.month}-{self.year}'
        r = requests.get(url).text
        return r


    def download_pic(self, list_):
        for i in list_:
            try:
                img = urllib.request.urlopen(i).read()

                out = open('pictures/'+i.split('/')[-1], 'wb')
                out.write(img)
                out.close
            except TypeError as e:
                print(e)


    def parse_picture(self):
        soup = bs(self.get_page(), 'lxml')
        hrefs_ = soup.find_all('a', href=True)

        list_ = []
        print(hrefs_)
        for i in hrefs_:
            print(i)
            try:
                if re.search('jpg|png', i.get('href')):
                    list_.append(i.get('href'))
            except TypeError as e:
                print(e)
        return self.download_pic(list_)



if __name__ == '__main__':
    a = Parser(sys.argv[1], sys.argv[2])
    a.parse_picture()
