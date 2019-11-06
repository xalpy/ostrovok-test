import re
import datetime
import sys
import urllib.request
import os

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs


class Parser:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.url = "https://www.smashingmagazine.com/"
        self.months_choices ={'january': '00', 'february': '01', 'march': '02',
                              'april': '03', 'may': '04', 'june': '05',
                              'jule': '06', 'august': '07', 'september': '08',
                              'october': '09', 'november': '10','december':'11'}

    def get_month_and_year(self):
        for i in self.months_choices:
            if self.month.lower() == i:
                return

    def get_page(self):
        self.get_month_and_year()
        if not os.path.isdir("./pictures"):
            os.mkdir("./pictures")
        for i in self.months_choices:
            if i == self.month.lower():
                self.month_code = self.months_choices[i]
                break
        url = f'{self.url}{self.year}/{self.month_code}/desktop-wallpaper-calendars-{self.month}-{self.year}'
        page = requests.get(url).text
        return page

    def download_pic(self, list_):
        for i in tqdm(list_):
            try:
                img = urllib.request.urlopen(i).read()
                with open('pictures/' + i.split('/')[-1], 'wb') as file:
                    file.write(img)
            except TypeError as e:
                print(e)

    def parse_picture(self):
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
                print(e)
        return self.download_pic(pictures_url)



if __name__ == '__main__':
    a = Parser(sys.argv[1], sys.argv[2])
    a.parse_picture()
