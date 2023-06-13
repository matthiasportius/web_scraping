import requests
import sqlite3
import time
from bs4 import BeautifulSoup

db = sqlite3.connect('chem.db')  # connect to database (+creates if non existant)
cur = db.cursor()  # creates cursor to execute SQL commands


# get cas from db


# url = f'https://abcr.com/de_de/catalogsearch/advanced/result/?cas={cas}'
url = "https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

abcr_data_price_r = soup.find_all('span', class_='price')  # class_: "sth" same as {"class": "sth"}
abcr_data_gram_r = soup.find_all('td', class_="align-right no-wrap")

abcr_data_price = [price.text[1:] for price in abcr_data_price_r]
abcr_data_gram = [gram.text.strip()[:-2] for gram in abcr_data_gram_r]

for p, g in zip(abcr_data_price, abcr_data_gram):
    cur.execute("INSERT OR IGNORE INTO prices VALUES(?, ?, ?, ?, ?)", ('1', "553-24-2", g, p, "https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2"))

db.commit()


# merck: search for G in text and for € in text
# make dict out of price and gram and replace url if price for same g is better (store every price-gram combination and make url behind that)
