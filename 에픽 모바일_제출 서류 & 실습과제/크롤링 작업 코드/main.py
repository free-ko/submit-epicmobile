import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib import parse
from datetime import datetime
import time
import threading

def crawling() :
    base_url = 'https://www.coupang.com/np/search?q={}&page={}'
    keyword = input("검색할 키워드 : ")
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'    
    }
    result_list = []
    url = base_url.format(keyword,1)
    print(url)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        print(soup)
        last_page = soup.select_one('a.btn-last').text.strip()
        print(last_page)


    error_cnt = 0
    for page in range(1, int(last_page)+1):
        url = base_url.format(keyword, page)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text)
            item_list = soup.select('ul#productList li a')
            for item in item_list:
                try:
                    link = item.select_one('img.search-product-wrap-img').get('src')
                    link = link.replace('//','')
                    if '.gif' in link:
                        continue
                    result_list.append([link])
                except:
                    error_cnt += 1



    curr = datetime.now().strftime('%Y-%m-%d')
    filename = '쿠팡조회결과_{}_{}.csv'.format(keyword,curr)
    df = pd.DataFrame(result_list, columns=['link'])
    df.to_csv(filename, index=False, encoding='utf-8')
    print('fail to save :', error_cnt)

    # 테스트로 3초 마다 함수 실행
    # 하루는 86400초
    threading.Timer(3, crawling).start()

crawling()