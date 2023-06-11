**requests** package to open website and get back its data
**beautifulsoup** package to sort collected data from website and get desited data

tipps for scraping:
    make it so that you only scrape what you could get as normal user (with sleep / wait functions to not bombard the server)
    don't overgo captcha or other barriers which are there for a reason
    don't just copy databases of a website (unspecific scraping of everything is not seen well)
    don't share databases (especially not for money)

other ways of scraping data are requests to an API which gives us the asked data 

websites to scrape:
    Indeed
    Tripadvisor
    Google
    Yellowpages
    Amazon
    Yahoo Financ
    Wikipedia
    Youtube

Most of youtube content is created via JS - not available by BeautifulSoup; can be accessed using re.findall and json.load(matches)

program that searches for chemical:
    can find out CAS if I give it a name
    searches for chemical on most used suppliers (VWR, Thermo Fischer, Merck, abcr, Carlroth, ...) and compares prices
    searches for NMR, MS spectra (or other useful info like melting point, molar mass, density, ...)

print request url (for example of smalles price): requests.get('url').url

databases to store data:
    MySQL:  good for websites, not so much features as Postgre SQL but faster, best for distributed setups and scaling (easy to upscale)
    PostgreSQL: good for complex queries/operations (supports multiple concurrent writers), highly customizable, best for data analysis applications (read + write is fast)
    SQLite: good for small amount of data, lightweight
    --> use SQLite for a start, then switch to Postgres