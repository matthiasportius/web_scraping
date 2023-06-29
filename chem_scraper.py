import requests
import sqlite3
import time
from bs4 import BeautifulSoup



def get_cas(chemicals: list[str]) -> None:
    for chem in chemicals:
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


def get_prices() -> None:
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


def save_to_text() -> None:
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



if __name__ == "__main__":
    db = sqlite3.connect('chem.db')  # connect to database (creates if non existant)
    cur = db.cursor()  # create cursor to execute SQL commands

    cur.execute("CREATE TABLE IF NOT EXISTS chemicals(name TEXT, cas TEXT PRIMARY KEY, molarmass REAL, nmr_url TEXT, ms_url TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS prices(cas_nr TEXT, gram REAL, price REAL, besprice_url TEXT, FOREIGN KEY(cas_nr) REFERENCES chem(cas))")

    CHEMICALS = ['Natriumchlorid', 'Neutralrot']  # preliminarily hardcoded

    get_cas(CHEMICALS)
    get_prices()
    save_to_text()
