# Relative Strength Index

import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data ={}

for ticker in tickers:
    temp = yf.download(ticker, period='1mo', interval='15m')
    temp.dropna(how='any', inplace=True)
    ohlcv_data[ticker] = temp
    
def RSI(DF, n=14):
    df = DF.copy()
    df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['change']>=0,df['change'],0)
    df['loss'] = np.where(df['change']<0,-1*df['change'],0)
    df['avgGain'] = df['gain'].ewm(alpha=1/n, min_periods = n).mean()
    df['avgLoss'] = df['loss'].ewm(alpha=1/n, min_periods = n).mean()
    df['RS'] = df['avgGain']/df['avgLoss']
    df['RSI'] = 100-(100/(1+df['RS']))
    return df['RSI']

for ticker in ohlcv_data:
    ohlcv_data[ticker]['RSI'] = RSI(ohlcv_data[ticker])

