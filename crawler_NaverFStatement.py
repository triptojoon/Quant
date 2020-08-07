import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

BASE_URL = 'https://finance.naver.com'

def crawl(code):
    req = requests.get(BASE_URL + '/item/main.nhn?code=' + code)
    page_soup = BeautifulSoup(req.text, 'lxml')
    finance_html = page_soup.select_one('div.cop_analysis')
    if finance_html == None:
        finance = pd.DataFrame(0, index = range(0,16), columns = range(0,10))
        finance_index = 'X'
        finance_date = 'X'
    else:
        finance_data = [item.get_text().strip() for item in finance_html.select('td')]
        if len(finance_data) < 2:
            finance = pd.DataFrame(0, index=range(0, 16), columns=range(0, 10))
            finance_index = 'X'
            finance_date = 'X'
        else:
            th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
            annual_date = th_data[3:7]
            quarter_date = th_data[7:13]

            finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]
            finance_data = [item.get_text().strip() for item in finance_html.select('td')]

            finance_data = np.array(finance_data)
            finance_data = np.where(finance_data == '', 0, finance_data)
            finance_data = np.where(finance_data == '-', 0, finance_data)
            finance_data.resize(len(finance_index), 10)

            finance_date = annual_date + quarter_date
            finance = pd.DataFrame(data=finance_data[0:, 0:], index = finance_index, columns = finance_date)

            #annual_finance = finance.iloc[:,:4]
            #quarter_finance = finance.iloc[:,4:]
    return finance,finance_index,finance_date


KRX_code = pd.read_csv('KRX_CODE.CSV', sep=',', encoding = 'CP949')
len_KRX = int(len(KRX_code))

sample_finance, sample_index, sample_date = crawl('005930')
code_index = ['CODE']
data_columns = code_index + sample_date

df_A = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_B = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_C = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_D = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_E = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_F = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_G = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_H = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_I = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_J = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_K = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_L = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_M = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_N = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_O = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)
df_P = pd.DataFrame(index=range(0,len_KRX), columns=data_columns)

for i in range(0,len_KRX):
    code = KRX_code['Code'].iloc[i]
    code = code.replace('A','')
    print(i,' - ',code)
    finance,X,Y = crawl(code)
    #매출액(억원)
    df_A.iloc[i,0] = code
    df_A.iloc[i,1:] = finance.iloc[0,:].values.tolist()
    #영업이익(억원)
    df_B.iloc[i, 0] = code
    df_B.iloc[i, 1:] = finance.iloc[1, :].values.tolist()
    #당기순이익(억원)
    df_C.iloc[i, 0] = code
    df_C.iloc[i, 1:] = finance.iloc[2, :].values.tolist()
    #영업이익률(%)
    df_D.iloc[i, 0] = code
    df_D.iloc[i, 1:] = finance.iloc[3, :].values.tolist()
    #순이익률(%)
    df_E.iloc[i, 0] = code
    df_E.iloc[i, 1:] = finance.iloc[4, :].values.tolist()
    #ROE(%)
    df_F.iloc[i, 0] = code
    df_F.iloc[i, 1:] = finance.iloc[5, :].values.tolist()
    #부채비율(%)
    df_G.iloc[i, 0] = code
    df_G.iloc[i, 1:] = finance.iloc[6, :].values.tolist()
    #당좌비율(%)
    df_H.iloc[i, 0] = code
    df_H.iloc[i, 1:] = finance.iloc[7, :].values.tolist()
    #유보율(%)
    df_I.iloc[i, 0] = code
    df_I.iloc[i, 1:] = finance.iloc[8, :].values.tolist()
    #EPS(원)
    df_J.iloc[i, 0] = code
    df_J.iloc[i, 1:] = finance.iloc[9, :].values.tolist()
    #PER(배)
    df_K.iloc[i, 0] = code
    df_K.iloc[i, 1:] = finance.iloc[10, :].values.tolist()
    #BPS(원)
    df_L.iloc[i, 0] = code
    df_L.iloc[i, 1:] = finance.iloc[11, :].values.tolist()
    #PBR(배)
    df_M.iloc[i, 0] = code
    df_M.iloc[i, 1:] = finance.iloc[12, :].values.tolist()
    #주당배당금(원)
    df_N.iloc[i, 0] = code
    df_N.iloc[i, 1:] = finance.iloc[13, :].values.tolist()
    #시가배당률(%)
    df_O.iloc[i, 0] = code
    df_O.iloc[i, 1:] = finance.iloc[14, :].values.tolist()
    #배당성향(%)
    df_P.iloc[i, 0] = code
    df_P.iloc[i, 1:] = finance.iloc[15, :].values.tolist()

with pd.ExcelWriter('DB_재무제표4개년.xlsx ') as writer:
    df_A.to_excel(writer,sheet_name = '매출액', index = False)
    df_B.to_excel(writer,sheet_name = '영업이익', index = False)
    df_C.to_excel(writer,sheet_name = '당기순이익', index = False)
    df_D.to_excel(writer,sheet_name = '영업이익률', index = False)
    df_E.to_excel(writer,sheet_name = '순이익률', index = False)
    df_F.to_excel(writer,sheet_name = 'ROE', index = False)
    df_G.to_excel(writer,sheet_name = '부채비율', index = False)
    df_H.to_excel(writer,sheet_name = '당좌비율', index = False)
    df_I.to_excel(writer,sheet_name = '유보율', index = False)
    df_J.to_excel(writer,sheet_name = 'EPS', index = False)
    df_K.to_excel(writer,sheet_name = 'PER', index = False)
    df_L.to_excel(writer,sheet_name = 'BPS', index = False)
    df_M.to_excel(writer,sheet_name = 'PBR', index = False)
    df_N.to_excel(writer,sheet_name = '주당배당금', index = False)
    df_O.to_excel(writer,sheet_name = '시가배당률', index = False)
    df_P.to_excel(writer,sheet_name = '배당성향', index = False)




