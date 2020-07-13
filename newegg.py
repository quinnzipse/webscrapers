import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import sys

if len(sys.argv) != 2:
    print('Input Invalid! Please provide search URL.')
    exit()

# record start time
start_time = time.time()

# create a file
f = open('output.txt', 'w')

my_url = 'https://www.newegg.com/p/pl?d=' + sys.argv[1].replace(' ', '+')

f.write('Data retrieved from: ' + my_url + '\n')

# open the conn, grab web page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

page_soup = page_soup.find('div', {'class': 'list-wrap'})

containers = page_soup.findAll('div', {'class': 'item-container'})

for container in containers:
    # print everything
    name = container.find('a', {'class': 'item-title'}).text.strip()
    f.write('\nProduct: ' + name + '\n------------------------\n')

    lists = container.findAll('ul')

    if len(lists) != 0:
        f.write('Features:\n------------------------\n')
        features = lists[0].findAll('li')
        for feature in features:
            f.write(feature.text + '\n')

        prices = lists[1].findAll('li')
        text = ''
        for price in prices:
            text += price.text.strip()

        text = text.replace('–', ' | ').replace('-', '| ')
        f.write('Price: ' + text + '\n')
    else:
        f.write('LISTS DIDN\'T LOAD\n')

total_time = str(time.time() - start_time)

print('Operation took: ' + total_time + 'ms')
f.write('\nOperation took: ' + total_time + 'ms')
f.close()
