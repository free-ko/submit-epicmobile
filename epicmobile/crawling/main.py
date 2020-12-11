import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib import parse
from datetime import datetime
import time
import threading

def crawling() :
    base_url = 'https://www.coupang.com/np/categories/417869/?page={}'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'    
    }
    result_list = []
    url = base_url.format(1)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text)



    error_cnt = 0
    for page in range(1, 18):
        url = base_url.format(page)
        print(url)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text)
            item_list = soup.select('ul#productList li a dl dt.image')
            for item in item_list:
                try:
                    link = item.select_one('img').get('src')
                    link = link.replace('//','')
                    if '.gif' in link:
                        continue
                    result_list.append([link])
                except:
                    error_cnt += 1


    # 크롤링 내역 저장
    curr = datetime.now().strftime('%Y-%m-%d')
    filename = '쿠팡조회결과_{}.csv'.format(curr)
    df = pd.DataFrame(result_list, columns=['link'])
    df.to_csv(filename, index=False, encoding='utf-8')
    print('fail to save :', error_cnt)

    # 테스트로 3초 마다 함수 실행
    # 하루는 86400초
    threading.Timer(5, crawling).start()

crawling()

