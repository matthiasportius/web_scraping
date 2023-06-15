import requests
import sqlite3
import time
from bs4 import BeautifulSoup

db = sqlite3.connect('chem.db')  # connect to database (+creates if non existant)
cur = db.cursor()  # creates cursor to execute SQL commands

# cur.execute("CREATE TABLE IF NOT EXISTS chemicals(name TEXT, cas TEXT PRIMARY KEY, molarmass REAL, nmr_url TEXT, ms_url TEXT)")
# cur.execute("CREATE TABLE IF NOT EXISTS prices(cas_nr TEXT, gram REAL, price REAL, besprice_url TEXT, FOREIGN KEY(cas_nr) REFERENCES chem(cas))")

# CHEMICALS = ['Natriumchlorid', 'Neutralrot']

# for chem in CHEMICALS:
#     url = f'https://de.wikipedia.org/wiki/{chem}'

#     response = requests.get(url)

#     soup = BeautifulSoup(response.text, 'html.parser')
#     wiki_data = soup.find('tbody')
#     table_data = wiki_data.text.split()
#     name = table_data[table_data.index('Name') + 1]
#     cas = table_data[table_data.index('CAS-Nummer') + 1]

#     cur.execute("INSERT OR IGNORE INTO chemicals (name, cas) VALUES(?, ?)", (name, cas))  # if conflict (because of unique cas value) then execute is ignored
#     db.commit()

#     time.sleep(3)


with open('results.txt', 'w') as f:
    chemical = cur.execute("SELECT name, cas FROM chemicals")
    for x in chemical.fetchall():
        name, cas = x
        f.write(f"Name: {name}   CAS: {cas}\n")
        vendor = cur.execute("SELECT gram, price, besprice_url FROM chemicals LEFT JOIN prices on cas_nr = ?", (cas,))
        for y in vendor.fetchall():
            gram, price, url = y
            if gram is not None:
                f.write(f"    {gram} g  :  {price} €   {url}\n")  # look up f strings and how to format
                # why is it written twice?






# Result:
# [('Natriumchlorid', '7647-14-5', None, None, None, None, None, None, None), 
# ('Neutralrot', '553-24-2', None, None, None, '553-24-2', 1.0, 63.5, 'https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2'), 
# ('Neutralrot', '553-24-2', None, None, None, '553-24-2', 10.0, 131.0, 'https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2'), 
# ('Neutralrot', '553-24-2', None, None, None, '553-24-2', 25.0, 84.9, 'https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2'), 
# ('Neutralrot', '553-24-2', None, None, None, '553-24-2', 25.0, 232.8, 'https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2'), 
# ('Neutralrot', '553-24-2', None, None, None, '553-24-2', 50.0, 63.4, 'https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2'), 
# ('Neutralrot', '553-24-2', None, None, None, '553-24-2', 250.0, 130.2, 'https://abcr.com/de_de/catalogsearch/advanced/result/?cas=553-24-2')]


# NEXT: implement (molar mass), nmr_url, ms_url, bestprice_url, clean up output (maybe write to text file)


# con.row_factory = sqlite3.Row   maybe nice, cause it's a superior row form
# select sth:
# for row in cur.execute(...): print(row) --> different than .fetchall

# search on some site like: if compound found - get ...