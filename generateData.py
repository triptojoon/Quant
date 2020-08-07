import pandas as pd
import FinanceDataReader as fdr
from time import time
from concurrent.futures import ProcessPoolExecutor

df_krx = fdr.StockListing('KRX')
df_krx['SymbolName'] = df_krx['Symbol'] + df_krx['Name']
print(df_krx)
codes = df_krx['SymbolName']

def getPrice(code):
    df_price = fdr.DataReader(code[:6], '2019-06-25', '2020-07-15')#주가 가져오기
    df_price =df_price[['Close']]
    df_price.columns = [code[6:]]
    return df_price

if __name__ == '__main__':
    start = time()
    pool = ProcessPoolExecutor(max_workers=10)
    results = list(pool.map(getPrice,codes))
    stocks = pd.concat(results, axis=1)
    end = time()
    print(end-start)
    stocks.to_excel('datas.xlsx')


