import requests
import sqlite3
import time
from bs4 import BeautifulSoup

db = sqlite3.connect('chem.db')  # connect to database (+creates if non existant)
cur = db.cursor()  # creates cursor to execute SQL commands

cur.execute("CREATE TABLE IF NOT EXISTS chemicals(name TEXT, cas TEXT PRIMARY KEY, molarmass REAL, nmr_url TEXT, ms_url TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS prices(cas_nr TEXT, gram REAL, price REAL, besprice_url TEXT, FOREIGN KEY(cas_nr) REFERENCES chem(cas))")

CHEMICALS = ['Natriumchlorid', 'Neutralrot']  # change to wanted chemicals (argparse - run after entering first chemical, error if not existant)

for chem in CHEMICALS:
    url = f'https://de.wikipedia.org/wiki/{chem}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    wiki_data = soup.find('tbody')
    table_data = wiki_data.text.split()
    name = table_data[table_data.index('Name') + 1]
    cas = table_data[table_data.index('CAS-Nummer') + 1]

    cur.execute("INSERT OR IGNORE INTO chemicals (name, cas) VALUES(?, ?)", (name, cas))  # if conflict (because of unique cas value) then execute is ignored
    db.commit()

    time.sleep(3)


cas = cur.execute("SELECT cas FROM chemicals").fetchall()
for c in cas:
    url = f'https://abcr.com/de_de/catalogsearch/advanced/result/?cas={c[0]}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    abcr_data_price_r = soup.find_all('span', class_='price')  # class_: "sth" same as {"class": "sth"}
    abcr_data_unit_r = soup.find_all('td', class_="align-right no-wrap")

    abcr_data_price = [price.text[1:] for price in abcr_data_price_r]
    abcr_data_unit = [gram.text.strip() for gram in abcr_data_unit_r]


    for p, g in zip(abcr_data_price, abcr_data_unit):
        cur.execute("INSERT OR IGNORE INTO prices VALUES(?, ?, ?, ?)", (c[0], g, p, url))

    db.commit()

    time.sleep(3)


with open('results.txt', 'w') as f:
    chemical = cur.execute("SELECT name, cas FROM chemicals").fetchall()
    for x in chemical:
        name, cas = x
        f.write(f"Name: {name}   CAS: {cas}\n")
        vendor = cur.execute("SELECT gram, price, besprice_url FROM prices WHERE cas_nr = ?", (cas,)).fetchall()

        for y in vendor:
            unit, price, url = y
            if unit is not None:
                f.write(f"    {unit}  :  {price} €   {url}\n")



# write into excel file instead of text
# NEXT: implement (molar mass), nmr_url, ms_url, bestprice_url


# con.row_factory = sqlite3.Row   maybe nice, cause it's a superior row form
# select sth:
# for row in cur.execute(...): print(row) --> different than .fetchall

# search on some site like: if compound found - get ...

# merck: search for G in text and for € in text
# make dict out of price and gram and replace url if price for same g is better (store every price-gram combination and make url behind that)
