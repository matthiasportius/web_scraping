import requests
import time
from bs4 import BeautifulSoup


URL = 'https://www.youtube.com/'

response = requests.get(URL)

print(response.text)
# soup = BeautifulSoup(response.text, 'html.parser')
# yt_data = soup.find('yt-formatted-string', {'id': 'video-title'})
# print(yt_data)