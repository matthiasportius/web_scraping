import requests
import sqlite3
import time
from bs4 import BeautifulSoup

db = sqlite3.connect('chem.db')  # connect to database (+creates if non existant)
cur = db.cursor()  # creates cursor to execute SQL commands

cur.execute("CREATE TABLE IF NOT EXISTS chem(name TEXT, cas TEXT UNIQUE, molarmass REAL, nmr_url TEXT, ms_url TEXT, bestprice_url TEXT)")

CHEMICALS = ['Natriumchlorid', 'Neutralrot']

for chem in CHEMICALS:
    url = f'https://de.wikipedia.org/wiki/{chem}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    wiki_data = soup.find('tbody')
    table_data = wiki_data.text.split()
    name = table_data[table_data.index('Name') + 1]
    cas = table_data[table_data.index('CAS-Nummer') + 1]

    cur.execute("INSERT OR IGNORE INTO chem (name, cas) VALUES(?, ?)", (name, cas))  # if conflict (because of unique cas value) then execute is ignored
    db.commit()

    time.sleep(3)


res = cur.execute("SELECT name, cas FROM chem")
print(f'{res.fetchall()}')

# con.row_factory = sqlite3.Row   maybe nice, cause it's a superior row form
# select sth:
# cur.execute("SELECT name, cas FROM chem ORDER BY name")
# for row in cur.execute(...): print(row) --> different than .fetchall