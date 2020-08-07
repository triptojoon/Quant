import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#KOSPI

df_finance = pd.read_excel('NaverFinance_KOSPI.xlsx')
df_price = pd.read_excel('datas.xlsx', index_col = 0)

MONTH_AGO = datetime(2020,6,26) + relativedelta(months = -1)
MONTH_AGO = MONTH_AGO.strftime('%Y-%m-%d')

YEAR_AGO = datetime(2020,6,26) + relativedelta(years = -1)
YEAR_AGO = YEAR_AGO.strftime('%Y-%m-%d')

price_month_ago = []
price_year_ago = []

for index, row in df_finance.iterrows():
    name = row['종목명']
    if name in df_price.columns:
        price_month_ago.append(df_price.loc[MONTH_AGO, name]) # datas에서 1달 전 주가 구하기
        price_year_ago.append(df_price.loc[YEAR_AGO, name]) # datas에서 1년 전 주가 구하기
    else:
        price_month_ago.append(0)
        price_year_ago.append(0)

df_finance['price_month_ago'] = price_month_ago # 1달 전 주가를 구해서 새로운 열으로 추가
df_finance['pirce_year_ago'] =price_year_ago # 1년전 주가를 구해서 새로운 열으로 추가

df_finance = df_finance[df_finance['price_month_ago'] != 0]

df_finance = df_finance.reset_index(drop = True)

df_finance['BPR'] = 1/df_finance['PBR'].astype(float)
df_finance['1/PER'] = 1/df_finance['PER'].str.replace(',','').astype(float)
df_finance['RANK_BPR'] = df_finance['BPR'].rank(method = 'max', ascending = False)
df_finance['RANK_1/PER'] = df_finance['1/PER'].rank(method = 'max', ascending = False)
df_finance['RANK_VALUE'] = (df_finance['RANK_BPR'] + df_finance['RANK_1/PER'])/2

df_finance = df_finance.sort_values(by = ['RANK_VALUE'])
df_finance = df_finance.reset_index(drop = True)

df_finance['현재가'] = df_finance['현재가'].str.replace(',','').astype(float)

# 1달 등락률 계산
df_finance['momentum_month'] = df_finance['현재가'] - df_finance['price_month_ago']
df_finance['1달 등락률'] = (df_finance['현재가'] - df_finance['price_month_ago']) / df_finance['현재가']

# 1년 등락률 계산
df_finance['momentum_year'] = df_finance['현재가'] - df_finance['pirce_year_ago']
df_finance['1년 등락률'] = (df_finance['현재가'] - df_finance['pirce_year_ago']) / df_finance['현재가']

df_finance['FINAL_MOMENTUM'] = df_finance['1년 등락률'] - df_finance['1달 등락률']
df_finance['RANK_MOMENTUM'] = df_finance['FINAL_MOMENTUM'].rank(method = 'max', ascending = False)

df_finance['FINAL_RANK'] = (df_finance['RANK_VALUE'] + df_finance['RANK_MOMENTUM'])/2
df_finance = df_finance.sort_values(by = ['FINAL_RANK'], ascending=[True])
df_finance = df_finance.reset_index(drop = True)

df_finance.to_excel('momentum_value_KOSPI.xlsx')


#KOSDAK

df_finance = pd.read_excel('NaverFinance_KOSDAK.xlsx')
df_price = pd.read_excel('datas.xlsx', index_col = 0)

MONTH_AGO = datetime(2020,6,26) + relativedelta(months = -1)
MONTH_AGO = MONTH_AGO.strftime('%Y-%m-%d')

YEAR_AGO = datetime(2020,6,26) + relativedelta(years = -1)
YEAR_AGO = YEAR_AGO.strftime('%Y-%m-%d')

price_month_ago = []
price_year_ago = []

for index, row in df_finance.iterrows():
    name = row['종목명']
    if name in df_price.columns:
        price_month_ago.append(df_price.loc[MONTH_AGO, name]) # datas에서 1달 전 주가 구하기
        price_year_ago.append(df_price.loc[YEAR_AGO, name]) # datas에서 1년 전 주가 구하기
    else:
        price_month_ago.append(0)
        price_year_ago.append(0)

df_finance['price_month_ago'] = price_month_ago # 1달 전 주가를 구해서 새로운 열으로 추가
df_finance['pirce_year_ago'] =price_year_ago # 1년전 주가를 구해서 새로운 열으로 추가

df_finance = df_finance[df_finance['price_month_ago'] != 0]

df_finance = df_finance.reset_index(drop = True)

df_finance['BPR'] = 1/df_finance['PBR'].astype(float)
df_finance['1/PER'] = 1/df_finance['PER'].str.replace(',','').astype(float)
df_finance['RANK_BPR'] = df_finance['BPR'].rank(method = 'max', ascending = False)
df_finance['RANK_1/PER'] = df_finance['1/PER'].rank(method = 'max', ascending = False)
df_finance['RANK_VALUE'] = (df_finance['RANK_BPR'] + df_finance['RANK_1/PER'])/2

df_finance = df_finance.sort_values(by = ['RANK_VALUE'])
df_finance = df_finance.reset_index(drop = True)

df_finance['현재가'] = df_finance['현재가'].str.replace(',','').astype(float)

# 1달 등락률 계산
df_finance['momentum_month'] = df_finance['현재가'] - df_finance['price_month_ago']
df_finance['1달 등락률'] = (df_finance['현재가'] - df_finance['price_month_ago']) / df_finance['현재가']

# 1년 등락률 계산
df_finance['momentum_year'] = df_finance['현재가'] - df_finance['pirce_year_ago']
df_finance['1년 등락률'] = (df_finance['현재가'] - df_finance['pirce_year_ago']) / df_finance['현재가']

df_finance['FINAL_MOMENTUM'] = df_finance['1년 등락률'] - df_finance['1달 등락률']
df_finance['RANK_MOMENTUM'] = df_finance['FINAL_MOMENTUM'].rank(method = 'max', ascending = False)

df_finance['FINAL_RANK'] = (df_finance['RANK_VALUE'] + df_finance['RANK_MOMENTUM'])/2
df_finance = df_finance.sort_values(by = ['FINAL_RANK'], ascending=[True])
df_finance = df_finance.reset_index(drop = True)

df_finance.to_excel('momentum_value_KOSDAK.xlsx')
