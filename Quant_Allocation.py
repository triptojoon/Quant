import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

BASE_URL = 'https://finance.naver.com/sise/dividend_list.nhn?&page='

start_code = '네이버금융 배당율 크롤링'
START_PAGE = 1

def main(code):
    # total_page를 가져오기 위한 requests
    res = requests.get(BASE_URL + str(START_PAGE))
    page_soup = BeautifulSoup(res.text, 'lxml')

    # total_page 가져오기
    total_page_num = page_soup.select_one('td.pgRR > a')
    total_page_num = int(total_page_num.get('href').split('=')[-1])

     # page마다 정보를 긁어오게끔 하여 result에 저장
    result = [crawl(str(page)) for page in range(1,total_page_num+1)]

    # page마다 가져온 정보를 df에 하나로 합침
    df = pd.concat(result, axis=0, ignore_index = True)

    # 크롤링한 것 중에 결측치가 있는 내용은 지워줍니다.
    # 4년이상 배당한 종목과 재무데이터 결측이 없는 종목만 남게됩니다.
    df = df[(df != '0').all(1)]
    df = df[(df != '').all(1)]
    df = df[(df != '-').all(1)]

    # 데이터프레임 형식을 맞춰줍시다
    df['현재가'] = df.현재가.str.replace(',','').astype(int)
    df['기준월'] = df.기준월.str.replace('.','년') + '월'
    df['배당금'] = df.배당금.str.replace(',','').astype(int)
    df['수익률(%)'] = df['수익률(%)'].str.replace(',','').astype(float)
    df['배당성향(%)'] = df['배당성향(%)'].str.replace(',','').astype(float)
    df['ROE(%)'] = df['ROE(%)'].str.replace(',','').astype(float)
    df['PER(배)'] = df['PER(배)'].str.replace(',','').astype(float)
    df['PBR(배)'] = df['PBR(배)'].str.replace(',','').astype(float)
    df['1년전'] = df['1년전'].str.replace(',', '').astype(int)
    df['2년전'] = df['2년전'].str.replace(',', '').astype(int)
    df['3년전'] = df['3년전'].str.replace(',', '').astype(int)

    # 수익률 6%이상 필터
    df = df[df['수익률(%)'] > 6]

    # ROE 10%이상 필터
    df = df[df['ROE(%)'] > 10]

    # 목표주가(배당수익률 3% 시점)
    df['목표주가'] = df['배당금'] / 0.03
    df['목표주가'] = df['목표주가'].astype(int)

    # 수익률 기준 랭킹 및 정리
    df['rank_수익률'] = df['수익률(%)'].rank(method = 'min', ascending = False)

    df = df.sort_values(by=['rank_수익률'], axis=0, ascending = True)
    df = df.reset_index(drop = True)

    # 엑셀로 내보내기
    print(df)
    df.to_excel('NaverFinance_Allocation.xlsx')

def crawl(page):
    res = requests.get(BASE_URL + str(page))
    page_soup = BeautifulSoup(res.text, 'lxml')
    # 크롤링할 table html 가져오기
    table_html = page_soup.select_one('table.type_1.tb_ty')

    # Column명 추출
    header_data = [item.get_text().strip() for item in table_html.select('thead th')][0:]
    del header_data[9]

    # 종목명 + 수치 추출 (a.title = 종목명, td.number = 기타 수치)
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x:
                                                                          (x.name == 'a' and
                                                                           'item' in x.get('href', [])) or
                                                                          (x.name == 'td' and
                                                                           'num' in x.get('class', []))
                                                                          )]
    inner_data = list(filter(None, inner_data))
    # page마다 있는 종목의 순번 가져오기

    no_data = 50
    number_data = np.array(inner_data)

    # 가로 x 세로 크기에 맞게 행렬화
    number_data.resize(no_data, len(header_data))

    # 한 페이지에서 얻은 정보를 모아 DataFrame으로 만들어 리턴
    df = pd.DataFrame(data= number_data, columns = header_data)
    return df

main(start_code)