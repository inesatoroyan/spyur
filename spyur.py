import requests
from bs4 import BeautifulSoup 
import time
import pandas as pd

#comment


base_url = 'https://www.spyur.am/am/home/advanced_search-'
all_links = [base_url + str(i) + '/?search=1&products_and_services=1&yp_cat3=459&from=by_home' for i in range(2,41)]
names=[]


for link in all_links:
    html = requests.get(link)
    page = html.content
    page=BeautifulSoup(page,'html.parser')
    for name in page.findAll('div', {'class':"company_name_new"}):
          for title in name.findAll('a'):
                names.append(title.get('href'))


names = list(set(names))

all_full = ['https://www.spyur.am'+ i for i in names]

zipo = {}


for link in all_full:
    html = requests.get(link)
    page = html.content
    page=BeautifulSoup(page,'html.parser')
    for i in page.findAll('li', {'class':"social"}):
        for link in i.findAll('a'):
            if (link.text == 'Facebook'):
                name = link.get('href')
    for z in page.findAll('h2', {'class':'company_name'}):
        link =z.text
    zipo[ name] = link


df = pd.DataFrame.from_dict(zipo,orient='index')
df.reset_index(level=0, inplace=True)
writer = pd.ExcelWriter('fb_restaurants.xlsx')
df.to_excel(writer)
writer.save()
