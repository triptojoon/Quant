import pandas as pd
import numpy as np

df_sales = pd.read_excel('DB_재무제표4개년.xlsx', sheet_name = '매출액', dtype = 'str', thousands = ',')
df_profit = pd.read_excel('DB_재무제표4개년.xlsx', sheet_name = '영업이익률', dtype = 'str', thousands = ',')

df_sales = df_sales.drop(['2019.03','2019.06','2019.09','2019.12.1','2020.03','2020.06(E)'], axis = 'columns')
df_profit = df_profit.drop(['2019.03','2019.06','2019.09','2019.12.1','2020.03','2020.06(E)'], axis = 'columns')

df_sales.columns = ['Code', 'Sales_17', 'Sales_18', 'Sales_19', 'Sales_20(E)']
df_profit.columns = ['Code', 'Profit_17', 'Profit_18', 'Profit_19', 'Profit_20(E)']


df_comb = pd.merge(df_sales,df_profit, on = 'Code', how = 'outer')

df_comb.iloc[:,1:] = df_comb.iloc[:,1:].astype('float')

df_comb['Sales_check'] = np.where((df_comb['Sales_17'] < df_comb['Sales_18']) & (df_comb['Sales_18'] < df_comb['Sales_19']), 'yes', 'no')
df_comb['Profit_check'] = np.where((df_comb['Profit_17'] < df_comb['Profit_18']) & (df_comb['Profit_18'] < df_comb['Profit_19']), 'yes', 'no')


df_select = df_comb.loc[(df_comb['Sales_check'] == 'yes') & (df_comb['Profit_check'] == 'yes')]

KRX_CODE = pd.read_csv('KRX_CODE.csv', sep=',', encoding = 'CP949')
KRX_CODE['Code'] = KRX_CODE['Code'].str.replace('A', '')

df_select = pd.merge(df_select,KRX_CODE, on = 'Code', how = 'left')

df_select = df_select.loc[:,['Company','Code','Sales_17','Sales_18','Sales_19','Sales_20(E)','Profit_17','Profit_18','Profit_19','Profit_20(E)']]


df_select['Sales_CAGR'] = (df_select['Sales_19'] - df_select['Sales_17'])**(1/3)-1
df_select = df_select.sort_values(by=['Sales_CAGR'], axis=0, ascending=False)
df_select = df_select.loc[(df_select['Profit_19'] > 10)]
df_select = df_select.loc[(df_select['Sales_CAGR'] > 10)]
df_select = df_select.reset_index(drop=True)

print(df_select)
df_select.to_excel('VALLIN_SteadyStocks.xlsx')