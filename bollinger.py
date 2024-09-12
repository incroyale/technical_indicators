# Bollinger Bands 

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period='1mo', interval='15m')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
    
def Boll_Band(DF, n=14):
    df = DF.copy()
    df['MB'] = df['Adj Close'].rolling(n).mean()
    df['UB'] = df['MB'] + 2*(df['Adj Close'].rolling(n).std(ddof=0))
    df['LB'] = df['MB'] - 2*(df['Adj Close'].rolling(n).std(ddof=0))
    df['BB_Width'] = df['UB'] - df['LB']
    return df[['MB', 'UB','LB','BB_Width']]

for ticker in ohlcv_data:
    ohlcv_data[ticker][['MB', 'UB','LB','BB_Width']] = Boll_Band(ohlcv_data[ticker], 20) 
    