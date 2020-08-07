import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
 
#KOSPI코드 파일 가져오기
df_code_KOSPI = pd.read_csv('KOSPI_CODE.CSV', sep=',', encoding = 'CP949')
#자본금 column 만들기
df_code_KOSPI['Share'] = 0
#자사주 column 만들기
df_code_KOSPI['Selfcount'] = 0

len_KRX = df_code_KOSPI.shape[0]

for i in range(0,len_KRX):
    CODE = df_code_KOSPI['Code'].iloc[i]
    BASE_URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=' + CODE + '&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
    res = requests.get(BASE_URL)
    page_soup = BeautifulSoup(res.text, 'lxml')
    FinanceS_html = page_soup.select_one('div#highlight_D_A.um_table')
    if FinanceS_html == None:
        continue
    else:
        inner_data = [item.get_text().strip() for item in FinanceS_html.find_all(lambda x:
                                                                                 (x.name == 'th' and 'clf' in x.get('class', [])) or
                                                                                 (x.name == 'td' and 'r' in x.get('class', [])))]
    if inner_data[85] == "":
        inner_data = 0
    else:
        inner_data = inner_data[85]
    df_code_KOSPI['Share'].iloc[i] = inner_data
    Stockcount_html = page_soup.select_one('div#svdMainGrid5.um_table')
    if Stockcount_html == None:
        continue
    else:
        inner_data2 = [item.get_text().strip() for item in Stockcount_html.find_all(lambda x:
                                                                                  (x.name == 'th' and 'clf' in x.get('class', [])) or
                                                                                  (x.name == 'td' and 'r' in x.get('class', [])))]
    if inner_data2[18] == "":
        inner_data2 = 0
    else:
        inner_data2 = inner_data2[18]

    df_code_KOSPI['Selfcount'].iloc[i] = inner_data2
    print(CODE, inner_data, inner_data2)

df_code_KOSPI.to_excel('Share_KOSPI.xlsx')

#KOSDAK코드 파일 가져오기
df_code_KOSDAK = pd.read_csv('KOSDAK_CODE.CSV', sep=',', encoding = 'CP949')
#자본금 column 만들기
df_code_KOSDAK['Share'] = 0
#자사주 column 만들기
df_code_KOSDAK['Selfcount'] = 0

len_KOSDAK = df_code_KOSPI.shape[0]

for i in range(0,len_KOSDAK):
    CODE = df_code_KOSDAK['Code'].iloc[i]
    BASE_URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=' + CODE + '&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
    res = requests.get(BASE_URL)
    page_soup = BeautifulSoup(res.text, 'lxml')
    FinanceS_html = page_soup.select_one('div#highlight_D_A.um_table')
    if FinanceS_html == None:
        continue
    else:
        inner_data = [item.get_text().strip() for item in FinanceS_html.find_all(lambda x:
                                                                                 (x.name == 'th' and 'clf' in x.get('class', [])) or
                                                                                 (x.name == 'td' and 'r' in x.get('class', [])))]
    if inner_data[85] == "":
        inner_data = 0
    else:
        inner_data = inner_data[85]
    df_code_KOSDAK['Share'].iloc[i] = inner_data
    Stockcount_html = page_soup.select_one('div#svdMainGrid5.um_table')
    if Stockcount_html == None:
        continue
    else:
        inner_data2 = [item.get_text().strip() for item in Stockcount_html.find_all(lambda x:
                                                                                  (x.name == 'th' and 'clf' in x.get('class', [])) or
                                                                                  (x.name == 'td' and 'r' in x.get('class', [])))]
    if inner_data2[18] == "":
        inner_data2 = 0
    else:
        inner_data2 = inner_data2[18]
    df_code_KOSDAK['Selfcount'].iloc[i] = inner_data2
    print(CODE, inner_data, inner_data2)

df_code_KOSDAK.to_excel('Share_KODAK.xlsx')