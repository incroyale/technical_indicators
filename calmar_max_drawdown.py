import yfinance as yf

tickers = ['AMZN', 'GOOG', 'MSFT']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period ='1y', interval='1d')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp

def max_dd(DF):    
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1+df['return']).cumprod()
    df['cum_roll_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_roll_max'] - df['cum_return']
    return (df['drawdown']/df['cum_roll_max']).max()

def CAGR(DF):
    df = DF.copy()
    df = df.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1 + df['return']).cumprod()
    n = len(df)/252
    CAGR = ((df['cum_return'][-1])**(1/n)) - 1
    return CAGR

def calmar(DF):
    df = DF.copy()
    return CAGR(df)/max_dd(DF)
    

for ticker in ohlcv_data:
    print(f"max drawdown of {ticker} = {max_dd(ohlcv_data[ticker])}")
    print(f"Calmar ratio of {ticker} = {calmar(ohlcv_data[ticker])}")