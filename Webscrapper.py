import requests
from bs4 import BeautifulSoup
from DB_Admin import *


class Webscrapper:
    def __init__(self, url):
        url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

    def get_lines(self, header, **kwargs):
        return self.soup.find_all(header, **kwargs)

    def get_line(self, header, **kwargs):
        return self.soup.find(header, **kwargs)

    def get_info(self, lines, *args, **kwargs):
        return lines.find(*args, **kwargs).text.strip()

info = {}

def scrapping():
    crypto_scrapper = Webscrapper("https://coinranking.com/")
    gold_scrapper = Webscrapper("https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF")
    silver_scrapper = Webscrapper("https://finance.yahoo.com/quote/SI%3DF?p=SI%3DF")

    first_10_crypto_lines = crypto_scrapper.get_lines('tr', class_='table__row table__row--click table__row--full-width')[:10]
    gold_line = gold_scrapper.get_line('div', id='quote-header-info')
    silver_line = silver_scrapper.get_line('div', id='quote-header-info')

    for line in first_10_crypto_lines:
        crypto_name = crypto_scrapper.get_info(line, 'a', class_='profile__link')
        crypto_price = crypto_scrapper.get_info(line, 'div', class_='valuta valuta--light').replace('$', '').strip()
        info[f"{crypto_name}"] = f"{crypto_price}"

    gold_name = gold_scrapper.get_info(gold_line, 'h1', class_='D(ib) Fz(18px)')
    gold_price = gold_scrapper.get_info(gold_line, 'fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')
    info[f"{gold_name}"] = f"{gold_price}"

    silver_name = silver_scrapper.get_info(silver_line, 'h1', class_='D(ib) Fz(18px)')
    silver_price = silver_scrapper.get_info(silver_line, 'fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')
    info[f"{silver_name}"] = f"{silver_price}"

    return info

if __name__ == "__main__":

    scrapping()

    db = Database("127.0.0.1", "root", "1234", "Exchange_DB")
    db.connect()

    for name, price in info.items():
        db.insert_into('Price', 'Asset_Name, Price', f'"{name}", "{price}"')


    db.commit()
    db.close()