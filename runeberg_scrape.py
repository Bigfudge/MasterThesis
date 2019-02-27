
import requests
from bs4 import BeautifulSoup
import re
import time



def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext


url = 'http://runeberg.org/status/ejsamman.html'
r = requests.get(url)
html_content = r.text
soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find_all('a')
links=table[15:-3]

for item in links:
    work= remove_tags(str(item))
    print(work)
    payload = {'mode': 'ocrtext', 'work': work}
    r = requests.get("http://runeberg.org/download.pl", params=payload)
    r.encoding = 'utf-8'
    filePath= "data/runeberg/"+work.replace("/","") +".txt"
    f = open(filePath, "w")
    f.write(r.text)
    time.sleep(1)
