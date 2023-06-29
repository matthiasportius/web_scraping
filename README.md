# Web Scraper

Here I tried out a little bit of web scraping using **requests** and **beautifulsoup**. I was just very interested in the topic and wanted to get a hang of the basics of these two packages. That is why I also did not make requests to an API, as I wanted to scrape right of the site to learn the basics. Of course, the code needs some (a lot) of adjustment, I listed some of them in the "TODO / Ideas" heading.
I also looked into databases and selenium while doing reasearch on web scraping. I put some notes to that in here as well.

## What are requests and beautifulsoup in simple terms?

**requests**: package to open website and get back its data  
**beautifulsoup**: package to sort collected data from website and get desired data

## Any basic tips on web scraping you have?

Make it so that you only scrape what you could get as a normal user.  
Implement sleep / wait functions to not bombard the server.  
Don't overgo captcha or other barriers which are there for a reason.  
Don't just copy databases of a website (unspecific scraping of everything is not seen well)  
Don't share databases you scraped (especially not for money!)  
Ask for permission if you feel uncertain.

## Some notes on databases and how they are commonly used

### MySQL  

- good for websites
- not so much features as Postgre SQL but faster
- best for distributed setups and scaling (easy to upscale)

### PostgreSQL

- good for complex queries/operations (supports multiple concurrent writers)
- highly customizable, best for data analysis applications (read + write is fast)

### SQLite

- good for small amount of data, lightweight
>Note: For small projects it is good to start with SQLite and then switch to Postgre if the database grows too large.

## Selenium vs Requests

As Selenium is a automated browser and Python Requests is a simple HTTP client, Selenium is the better option if you are scraping dynamic pages that require the page to be client side rendered before showing all the data. This is typical for websites that use modern web frameworks like AngularJS, ReactJS, VueJS, etc.

requests for:
- scraping at large scale/fast
- scraping API endpoints

selenium for: 
- rendering dynamic pages, when lot of interaction (click, scroll,...) with website is necessary
- automated bots that work behind logins
- screenshots of pages
- heavily protected websites

## TODO / Ideas

- Replace hardcoded search-values with *argparse* functionality or some kind of GUI 
- Check if wikipedia-url exists (name is entered correctly)
- Add cookie to `get_prices()` abcr `requests.get()` call, since it does not work if the site has not been visited before.
- Change output to text to output to .csv (Excel files are just better)
- Add scraping option for Merck (search for "G" and for "€" in text)
- Add scraping option for VWR, Thero Fischer, Carlroth, ...
- compare prices of suppliers and return cheapest (maybe dict with gram:(price, url) and replace url if price for same g is better)
- scrape melting point, molar mass and density from wikipedia
- look for sites that have NMR and/or MS data that can be scraped
- maybe use `sqlite3.Row`
- maybe `for row in cur.execute(...):` faster as `fetchall()`
