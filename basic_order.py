from smartapi import SmartConnect
import os
import urllib
import json
from pyotp import TOTP

key_path = r"E:\OneDrive\Desktop\f"
os.chdir(key_path)

key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()

instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(instrument_url)
instrument_list = json.loads(response.read())

def token_lookup(ticker, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == "EQ":
            return instrument["token"]

def place_limit_order(instrument_list,ticker,buy_sell,price,quantity,exchange="NSE"):
    params = {
                "variety":"NORMAL",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"LIMIT",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "price":price,
                "quantity":quantity
                }
    order = obj.placeOrder(params)
    return order

def place_market_order(instrument_list,ticker,buy_sell,quantity,sl=0,sqof=0,exchange="NSE"):
    params = {
                "variety":"NORMAL",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "quantity":quantity
                }
    order = obj.placeOrder(params)
    return order


place_limit_order(instrument_list, "HDFC", "BUY", 2400, 1)















