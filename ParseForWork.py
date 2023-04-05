import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup


class ParsePage:
    def __init__(self):
        self.AllInfo = {"products" : []}
        self.mainLink = 'https://mebsleep.ru'
        for i in range(1,5):
            self.linkPage = f"https://mebsleep.ru/category/krovat_detskaya/?page={i}&brands%5B0%5D=38750"
            self.fullData = requests.get(self.linkPage).text
            self.parseData = BeautifulSoup(self.fullData, 'html.parser')
            self.item_links = self.getLink()
            self.getDataAboutItem()
        self.write_to_json(self.AllInfo)

    def getLink(self):
        links = []
        li = self.parseData.body.findAll('li', attrs={'class': 'products__item'})
        for item in li:
            links.append(item.find('a', attrs={'class': 'products__link'}).get('href'))
        return links

    def getDataAboutItem(self):
        for link in self.item_links:
            info = {}
            fullPage = requests.get(self.mainLink + link + "?cart=1").text
            parseData = BeautifulSoup(fullPage, "html.parser")

            info['Name'] = parseData.find('h1').text
            info['Price'] = parseData.find('span', attrs={"class": "product__price"}).text
            info['Description'] = parseData.find('div', attrs={"class": "contentDescription"}).text
            info['Size'] = [size.text for size in parseData.find('select', attrs={"class": "sku-feature"}).findAll('option')]
            info['images'] = [self.mainLink +img.get("src") for img in parseData.find('div', attrs={"class": "product__images"}).findAll('img')]

            pprint(info)
            self.AllInfo['products'].append(info)

    @staticmethod
    def write_to_json(data):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    ParsePage = ParsePage()
