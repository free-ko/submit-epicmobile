import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib import parse
from datetime import datetime
import time

base_url = 'https://www.coupang.com/np/categories/417869/?page={}'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'    
}
result_list = []
url = base_url.format(1)
print(url)
res = requests.get(url, headers=headers)
if res.status_code == 200:
    soup = BeautifulSoup(res.text)
    print(soup)
    last_page = soup.select_one(".selected").text.strip()
    print(last_page)


error_cnt = 0
cp_url = 'https://www.coupang.com/417869/'
for page in range(1, int(last_page)+1):
    url = base_url.format(page)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        item_list = soup.select('ul#productList li dl.baby-product-wrap dt.image img')
        for item in item_list:
            try:
                images = item.select_one("src")
                result_list.append(images)
            except:
                error_cnt += 1


# 크롤링 내역 저장
curr = datetime.now().strftime('%Y-%m-%d')
filename = '쿠팡조회결과_{}_{}.csv'.format(curr)
df = pd.DataFrame(result_list, columns=['title','link'])
df.to_csv(filename, index=False, encoding='utf-8')
print('fail to save :', error_cnt)