import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np


url = requests.get('https://hashtagbasketball.com/nba-defense-vs-position')
soup = BeautifulSoup(url.text, 'html.parser')
table = soup.find('div', attrs= {'class' : 'table-responsive'}).find('div').find('table').find('tbody')
rows = table.find_all('tr')
rowsValue = rows.find_all()
rowsRank = rows.find_all()
