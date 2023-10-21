from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import pandas as pd
import lxml
import csv


def get_link():
    link_list = []
    for i in range(1, 201):
        link = f"https://www.unegui.mn/avto-mashin/-avtomashin-zarna/?page={i}"
        link_list.append(link)
    return link_list


car_link_list = []
n = get_link()


def get_car_url(url, car_link_list):
    ua = UserAgent()
    fake_user = {"user-agent": ua.random}
    response = requests.get(url=url, headers=fake_user)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    dt = soup.find('div', class_="list-announcement-assortiments")
    try:
        vip = dt.find('div', class_='list-title__top')
    except Exception as e:
        vip = None
    try:
        special = dt.find('div', class_='list-title__top')
    except Exception as e:
        special = None

    if vip != None and vip.text == 'VIP зар':
        links = dt.find('div', class_='list-title__top-container')
        for x in links.find_all('div', class_='announcement-container announcement-container--top'):
            link = x.find('a', class_='announcement-block__title')['href']
            car_link_list.append(f"https://www.unegui.mn/{link}")
    elif special != None and special.text == 'Онцгой зар':
        links = dt.find('div', class_='list-title__top-container')
        for x in links.find_all('li', class_='announcement-container'):
            link = x.find('a', class_='mask')['href']
            # print(f'онцгой{link}')
            car_link_list.append(f"https://www.unegui.mn/{link}")
    else:
        try:
            dt = dt.find('ul', class_='list-simple__output js-list-simple__output')

            for x in dt.find_all('li', class_='announcement-container'):
                link = x.find('a', class_='mask')['href']
                # print(f'Энгийн зар{link}')
                car_link_list.append(f"https://www.unegui.mn/{link}")
        except Exception as e:
            print(e)

    return car_link_list


for n, url in enumerate(n):
    print(f"working...{n} {url}")
    get_car_url(url, car_link_list)
print('Link done!')
data_link = pd.DataFrame(columns=['link'])
counter = 0
for n, url in enumerate(car_link_list):
    data_link.loc[n] = url
data_link.to_csv('car_links.csv', mode='w', index=False)
