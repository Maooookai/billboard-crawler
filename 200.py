import os.path
import platform
from datetime import datetime

import bs4
import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def file_check(system_type):
    if os.path.exists('200-' + str(datetime.now().date()) + '.xlsx'):
        print('Detected file: 200-' + str(datetime.now().date()) + '.xlsx\nAre you sure to delete then recreate? (y/n)')
        key = input()
        if key == 'y':
            os.remove('200-' + str(datetime.now().date()) + '.xlsx')
    if system_type != 'Windows' and not os.path.exists('chromedriver'):
        return False,
    if system_type == 'Windows' and not os.path.exists('chromedriver.exe'):
        return False
    return True


def crawl(chromedriver_location):
    driver = webdriver.Chrome(service=Service(chromedriver_location))
    print('loading page...')
    driver.get("https://www.billboard.com/charts/billboard-200/")
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, 'html.parser')
    all_albums = soup.find_all('div', class_='o-chart-results-list-row-container')
    billboard_200 = []
    for album in all_albums:
        span_data = album.findAll('span', class_='c-label')
        if 'NEW' in span_data[1].text.strip() or 'RE' in span_data[1].text.strip():
            this_week = span_data[0].text.strip()
            artist = span_data[3].text.strip()
            last_week = span_data[7].text.strip()
            peak_pos = span_data[8].text.strip()
            wks_on_chart = span_data[9].text.strip()
            if wks_on_chart != '1':
                trend = 'RE-ENTER'
            else:
                trend = 'NEW'
        else:
            this_week = span_data[0].text.strip()
            artist = span_data[1].text.strip()
            last_week = span_data[2].text.strip()
            peak_pos = span_data[3].text.strip()
            wks_on_chart = span_data[4].text.strip()
            if int(this_week) < int(last_week):
                trend = 'UP ↑'
            elif int(this_week) > int(last_week):
                trend = 'DOWN ↓'
            elif int(this_week) == int(last_week):
                trend = 'STAY →'
            else:
                trend = ''
        title = album.find('h3', {'id': 'title-of-a-story'}).text.strip()
        data = [trend, title, artist, this_week, last_week, peak_pos, wks_on_chart]
        print(data)
        billboard_200.append(data)
    driver.quit()
    return billboard_200


def insert_data(data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Trend'
    sheet['B1'] = 'Album'
    sheet['C1'] = 'Artist'
    sheet['D1'] = 'This Week'
    sheet['E1'] = 'Last Week'
    sheet['F1'] = 'Peak Position'
    sheet['G1'] = 'Weeks on Chart'

    for row in data:
        sheet.append(row)

    workbook.save('200-' + str(datetime.now().date()) + '.xlsx')


if __name__ == '__main__':
    '''This program crawls current Billboard 200.
    Website: https://www.billboard.com/charts/billboard-200/
    '''
    current_system = platform.system()
    if not file_check(current_system):
        print('chromedriver not found, please make sure that the newest Google Chrome is installed '
              'and download the correct version to project folder from')
        print('https://chromedriver.chromium.org/downloads')
    if current_system == 'Windows':
        result = crawl('./chromedriver.exe')
    else:
        result = crawl('./chromedriver')
    insert_data(result)
