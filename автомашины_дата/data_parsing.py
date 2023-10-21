from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import pandas as pd
import csv
import lxml
import numpy as np
from tqdm import tqdm


def apply_pattern(arr2, arr3, pattern):
    result = [np.nan] * len(pattern)

    for i, p in enumerate(pattern):
        if p in arr2:
            index = arr2.index(p)
            result[i] = arr3[index]

    return result


urls = pd.read_csv('car_links.csv')
urls = urls['link'].values.tolist()

header = ['Машины марк', "Үнэ", "Моторын багтаамж", "Хурдны хайрцаг", "Хүрд",
          "Төрөл", "Өнгө", "Үйлдвэрлэсэн он", "Орж ирсэн он", "Хөдөлгүүр", "Дотор өнгө",
          "Лизинг", "Хаяг", "Хөтлөгч", "Явсан", "Нөхцөл", "Хаалга"]

pattern = ['Урьдчилсан төлбөрийн хэмжээ', 'Мотор багтаамж', 'Хурдны хайрцаг', 'Хүрд', 'Төрөл', 'Өнгө',
           'Үйлдвэрлэсэн он', 'Орж ирсэн он', 'Хөдөлгүүр', 'Дотор өнгө', 'Лизинг', 'Хаяг байршил', 'Хөтлөгч', 'Явсан',
           'Нөхцөл', 'Хаалга']

with open('unegui_cars_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(header)


def crawl_data(url):
    row = []
    arr1 = []
    arr2 = []
    ua = UserAgent()
    fake_useragent = {'user-agent': ua.random}
    response = requests.get(url=url, headers=fake_useragent)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    container = soup.find('div', class_='announcement-content-container')
    table = soup.find('div', class_='announcement-characteristics clearfix')

    # TODO mark
    try:
        car_mark = container.find('h1', class_='title-announcement').text.strip()
    except Exception as e:
        car_mark = np.nan
    row.append(car_mark)

    try:
        table = table.find('ul', class_='chars-column')
        for i in table.find_all('li'):
            data = i.text.split(":")
            arr1.append(data[0].strip())
            arr2.append(data[1].strip())

        array = apply_pattern(arr1, arr2, pattern)
        row.extend(array)
    except Exception as e:
        print(e)

    try:
        price = soup.find('div', class_='announcement-price').text
        price = price.strip().splitlines()
        price = price[0]
        if len(row) > 1:
            row[1] = price
    except Exception as e:
        if len(row) > 1:
            row[1] = row[1]
    return row


for url in tqdm(urls):
    a = crawl_data(url)
    if len(header) == len(a):
        file = open('unegui_cars_data.csv', 'a', encoding='utf-8-sig', newline='')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(a)
file.close()
print(f'Done!!!')
