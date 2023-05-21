from datetime import datetime

import openpyxl
import requests
from bs4 import BeautifulSoup


def insert_data(data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Artist'
    sheet['B1'] = 'Album'
    sheet['C1'] = 'This Week'
    sheet['D1'] = 'Last Week'
    sheet['E1'] = 'Sales'

    for row in data:
        sheet.append(row)

    workbook.save('HDD-' + str(datetime.now().date()) + '.xlsx')


def format_number(num):
    suffixes = ['', 'k', 'M', 'B', 'T']
    magnitude = 0
    while num >= 1000:
        num /= 1000
        magnitude += 1
    return f'{num:.1f}{suffixes[magnitude]}'


def crawl():
    url = 'https://hitsdailydouble.com/sales_plus_streaming'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_albums = soup.find('table', class_='hits_album_chart')

    hdd = []
    artist_and_album = all_albums.find_all('span', class_='hits_album_chart_item_details_full_artist')
    this_weeks = all_albums.find_all('td', class_='hits_album_chart_full_tw')
    last_weeks = all_albums.find_all('td', class_='hits_album_chart_full_lw')
    sales = all_albums.find_all('td', class_='hits_album_chart_item_top_details_full_sales chart_tweak col_sales')
    for i in range(0, 50):
        one_album = artist_and_album[i].text.strip()
        split = one_album.split('|')
        artist = split[0].strip()
        album = split[1].strip()
        last_week = last_weeks[i].text.strip()
        this_week = this_weeks[i].text.strip()
        sale = format_number(int(sales[i].text.strip().replace(',', '')))
        data = [artist, album, this_week, last_week, sale]
        print(data)
        hdd.append(data)
    return hdd


if __name__ == '__main__':
    insert_data(crawl())
