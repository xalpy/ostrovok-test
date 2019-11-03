import requests

from bs4 import BeautifulSoup as bs

import urllib.request

import re

import datetime


class Parser:
    def get_month_and_year(self):
        self.months_choices = []
        self.month = input('Введите месяц: ')
        self.year = input('Введите год: ')
        for i in range(1,13):
            if i-1 < 10:
                self.months_choices.append(('0'+str(i-1), datetime.date(2008,
                                            i, 1).strftime('%B')))
            else:
                self.months_choices.append((i-1, datetime.date(2008,
                                            i, 1).strftime('%B')))

        for i in self.months_choices:
            if self.month.capitalize() in i[1]:
                return
        print('месяц или год не соответсвуют стандарту:\n\
пример(месяц): may, june, october\n\
пример(год): 2010, 2017')
        return self.get_month_and_year()


    def get_page(self):
        self.get_month_and_year()
        for i in self.months_choices:
            if i[1] == self.month.capitalize():
                self.month_code = i[0]
                break

        url = f'https://www.smashingmagazine.com/{self.year}/{self.month_code}\
/desktop-wallpaper-calendars-{self.month}-{self.year}'
        r = requests.get(url).text
        return r


    def download_pic(self, list_):
        for i in list_:
            img = urllib.request.urlopen(i).read()
            out = open('pictures/'+i.split('/')[-1], 'wb')
            out.write(img)
            out.close


    def parse_picture(self):
        soup = bs(self.get_page(), 'lxml')
        li_ = soup.find_all('li')

        list_ = []
        for i in li_:
            try:
                if bool(re.search('jpg', i.a.get('href'))) \
                or bool(re.search('png', i.a.get('href'))):
                    list_.append(i.a.get('href'))
            except:
                pass
        return self.download_pic(list_)



if __name__ == '__main__':
    a = Parser()
    a.parse_picture()
