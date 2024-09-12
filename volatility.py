import yfinance as yf
import numpy as np

tickers = ['AMZN', 'GOOG', 'MSFT']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period ='1y', interval='1d')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
    
def volatility(DF):
    df = DF.copy()    
    df['return']= df['Adj Close'].pct_change()
    vol = df['return'].std() * np.sqrt(252) 
    return vol

for ticker in ohlcv_data:
    print(f"Volatility of {ticker} = {volatility(ohlcv_data[ticker])} ")
        