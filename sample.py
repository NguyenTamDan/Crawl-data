import requests
from bs4 import BeautifulSoup
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
import pandas as pd

url = 'https://gdt.gov.vn/wps/portal/home/qdcchd1'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = []
for link in soup.find_all('a')[21:84]:
    urls.append(link.get('href'))
    #print(link.get('href'))

for i in range(len(urls)):
    url = urls[i]
    url = 'https://gdt.gov.vn/wps/portal/home/qdcchd1/list?1dmy&current=true&urile=wcm:path:/' + url[58:len(url)-15] + '/site/sa-cmcchd'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tb_data = soup.find_all('table')
    #print(tb_data)

def get_url(url, page):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # some code with th / tr / td
    tb_data = soup.find_all('table')
    def url_get_contents(url):
        req = urllib.request.Request(url=url)
        f = urllib.request.urlopen(req)
        return f.read()

    xhtml = url_get_contents(url).decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    pprint(p.tables)

    print("\n\nPANDAS DATAFRAME\n")
    a = pd.DataFrame(p.tables).T
    a = a.rename(columns={0: 'name'})
    a[['Ngày quyết định', 
    'Mã số thuế', 
    'Tên người nộp Thuế', 
    'Quyết định cưỡng chế', 
    'Thông báo hóa đơn tiếp tục có giá trị sử dụng']] = pd.DataFrame(a.name.tolist(), index= a.index)
    a.drop(["name"], axis = 1, inplace = True)
    b = a.drop([0])
    file_name = 'Data1.xlsx'
    b.to_excel(file_name)
    
    # next page
    next_page = 'page ' + str(page + 1)
    print(next_page)

    for link in soup.find_all('a'):
        title = link.get('title')
        if title and title.find(next_page) > 0:
            print(r.url + link.get('href'))
            get_url(r.url + link.get('href'), page + 1)
path = 'https://gdt.gov.vn/wps/portal/home/qdcchd1'
resp = requests.get(path)
soup = BeautifulSoup(resp.text, 'html.parser')

for link in soup.find_all('a')[21:84]:
    url = link.get('href')
    get_url('https://gdt.gov.vn/wps/portal/home/qdcchd1/list?1dmy&current=true&urile=wcm:path:/' + url[58:len(url)-15] + '/site/sa-cmcchd', 1)