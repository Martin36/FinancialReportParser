import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pprint
import re
import time
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
pp = pprint.PrettyPrinter(indent=2)
init_url = "https://vp201.alertir.com/v2/en/reports"
base_url = "https://vp201.alertir.com"
agent = {"User-Agent":"Mozilla/5.0"}
# init_url = "https://www.hoistfinance.com/investors/reports-and-presentations/"
# print(res.text)
names = []

def get_report_urls(urls):
  # Extract report urls
  report_urls = list(dict.fromkeys([url for url in urls if re.search(r'/v2/en/interim-report|/v2/en/annual-report/', url)]))
  return report_urls

def get_nav_urls(urls):
  # Extract internal navigation links and remove duplicates
  nav_urls = list(dict.fromkeys([url for url in urls if re.search(r'page=', url)])) 
  return nav_urls

def get_all_links(url):
  urls = []
  res = requests.get(url, headers=agent)
  soup = bs(res.text, features="html.parser")
  # Get all the links on the page
  for i, link in enumerate(soup.findAll('a')):
    href = link.get('href')
    urls.append(href)
  return urls

def download_pdfs(urls):
  link_text_re = re.compile(r'Report|report')
  for i, url in enumerate(urls):
    full_url = base_url + url
    res = requests.get(full_url, headers=agent)
    soup = bs(res.text, features="html.parser")
    for link in soup.findAll('a', href=True, text=link_text_re):
      href = link.get('href')
      name = link.text.strip()
      if ".pdf" not in href:
        continue
      res = requests.get(base_url + href, headers=agent)
      with open(DIR_PATH + '/pdfs/' + name + '.pdf', 'wb') as file:
        print("Downloading file:" + name)
        file.write(res.content)
        file.close()
    time.sleep(1)






urls = get_all_links(init_url)
nav_urls = get_nav_urls(urls)
report_urls = get_report_urls(urls)
for i, nav_url in enumerate(nav_urls):
  links = get_all_links(base_url + nav_url)
  report_links = get_report_urls(links)
  report_urls = report_urls + report_links

download_pdfs(report_urls)


pp.pprint(report_urls)


