import requests
import sqlite3
import time
from bs4 import BeautifulSoup

db = sqlite3.connect('chem.db')  # connect to database (+creates if non existant)
cur = db.cursor()  # creates cursor to execute SQL commands

cur.execute("CREATE TABLE IF NOT EXISTS chem(chemid INTEGER PRIMARY KEY, name TEXT, cas TEXT UNIQUE, molarmass REAL, nmr_url TEXT, ms_url TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS prices(chempriceid INTEGER, cas_nr TEXT, gram REAL, price REAL, besprice_url TEXT, FOREIGN KEY(chempriceid) REFERENCES chem(chemid))")

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


res = cur.execute("SELECT * FROM chem")
res2 = cur.execute("SELECT * FROM prices")
print(f'{res.fetchall()}')
print(f'{res2.fetchall()}')


# NEXT: implement (molar mass), nmr_url, ms_url, bestprice_url, clean up output (maybe write to text file)


# con.row_factory = sqlite3.Row   maybe nice, cause it's a superior row form
# select sth:
# cur.execute("SELECT name, cas FROM chem ORDER BY name")
# for row in cur.execute(...): print(row) --> different than .fetchall

# search on some site like: if compound found - get ...