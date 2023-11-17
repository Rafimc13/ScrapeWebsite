import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from langdetect import detect



warmane_url = "https://forum.warmane.com/forumdisplay.php?f=20&page=1"


response = requests.get(warmane_url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)



posts = soup.find_all('a', class_='title')
for post in posts:
    print(post.get_text())

authors = soup.find_all('dl', class_='threadauthor td')

my_authors = []
pattern = re.compile(r'\n')
for author in authors:
    my_authors.append(pattern.sub("", author.get_text()))



pattern = r'thread_\d{6}'
threads = re.findall(pattern, html_content)

my_threads= []
pattern = re.compile(r"thread_")
for thread in threads:
    my_threads.append(pattern.sub("", thread))


each_thread_url = 'https://forum.warmane.com/showthread.php?t='

dates = []
replies = []
for id in my_threads:
    repsonse2 = requests.get(each_thread_url+id)
    html_content = repsonse2.text
    soup = BeautifulSoup(html_content, 'html.parser')
    dates.append(soup.find(class_ = 'date').get_text())
    replies.append(soup.find_all('div', class_ ='content'))

my_dates = []
pattern = re.compile(r" \xa0")
for date in dates:
    my_dates.append(pattern.sub("", date))











