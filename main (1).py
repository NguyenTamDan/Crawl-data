import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_url(dn, city, url, page):
    print (city, ': ', page, ': ', len(response))
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # some code with th / tr / td; return if not found
    cnt = 0
    for table in soup.find_all('table'):
        for row in table.find_all('tr')[1:]:
            data = [city] + [i.text for i in row.find_all('td')]
            data_str = ''.join(data)

            if data_str in data_set:
                cnt += 1
            else:
                response.append(data)
                data_set.add(data_str)

    # god bless you
    if cnt == 3:
        dn -= 1
        if dn < 0:
            return

    # next page
    index = url.find('=CTX')
    if index > 0:
        last_id = url[:index].rfind('!')
        url = url[:last_id + 1] + str(page + 1) + url[index:]
        get_url(dn, city, url, page + 1)
    else: # page 2 only
        for link in soup.find_all('a'):
            title = link.get('title')
            if title and title.find('page 2') > 0:
                get_url(dn, city, resp.url + link.get('href'), page + 1)


path = 'https://gdt.gov.vn/wps/portal/home/qdcchd1'
resp = requests.get(path)
soup = BeautifulSoup(resp.text, 'html.parser')

response = []
data_set = set()

for link in soup.find_all('a')[23:84]:
    url = link.get('href')
    get_url(2, link.text[9:],
            'https://gdt.gov.vn/wps/portal/home/qdcchd1/list?1dmy&current=true&urile=wcm:path:/'
             + url[58:len(url) - 15] + '/site/sa-cmcchd', 1)
    break

columns = [
    'Tỉnh thành',
    'Ngày quyết định', 
    'Mã số thuế', 
    'Tên người nộp Thuế', 
    'Quyết định cưỡng chế', 
    'Thông báo hóa đơn tiếp tục có giá trị sử dụng'
    ]
frame = pd.DataFrame(response, columns= columns)
frame.to_excel('An Giang.xlsx')

