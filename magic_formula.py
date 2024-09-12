import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ['AAPL', 'FB', 'CSCO', 'INFY.NS', '3988.HK']
income_statement_dict = {}
balance_sheet_dict = {}
cashflow_dict = {}
headers = {'User-Agent':'Chrome/96.0.4664.110'}

for ticker in tickers:
    # Income Statement
    income_statement = {}
    table_title = {}
    url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'lxml')
    tabl = soup.find_all('div', {'class':"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all('div', {'class':"D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator='_').split('_')[0]] = top_row.get_text(separator='_').split('_')[1:]
        rows = t.find_all('div', {'class':"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            income_statement[row.get_text(separator='_').split('_')[0]] = row.get_text(separator='_').split('_')[1:]
        temp = pd.DataFrame(income_statement).T
        temp.columns = table_title['Breakdown']
        income_statement_dict[ticker] = temp
        
    # Balance Sheet
    balance_sheet = {}
    table_title = {}
    url = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'lxml')
    tabl = soup.find_all('div', {'class':"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all('div', {'class':"D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator='_').split('_')[0]] = top_row.get_text(separator='_').split('_')[1:]
        rows = t.find_all('div', {'class':"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            balance_sheet[row.get_text(separator='_').split('_')[0]] = row.get_text(separator='_').split('_')[1:]
        temp = pd.DataFrame(balance_sheet).T
        temp.columns = table_title['Breakdown']
        balance_sheet_dict[ticker] = temp
        
    # Cash Flow
    cash_flow = {}
    table_title = {}
    url = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'lxml')
    tabl = soup.find_all('div', {'class':"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all('div', {'class':"D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator='_').split('_')[0]] = top_row.get_text(separator='_').split('_')[1:]
        rows = t.find_all('div', {'class':"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            cash_flow[row.get_text(separator='_').split('_')[0]] = row.get_text(separator='_').split('_')[1:]
        temp = pd.DataFrame(cash_flow).T
        temp.columns = table_title['Breakdown']
        cashflow_dict[ticker] = temp

for ticker in tickers:
    for col in income_statement_dict[ticker].columns:
        income_statement_dict[ticker][col] = income_statement_dict[ticker][col].str.replace(',|-','')
        income_statement_dict[ticker][col] = pd.to_numeric(income_statement_dict[ticker][col], errors = 'coerce')
    
# Scrape Key Statistics
table = soup.find_all('div', {'class':"W(100%) Bdcl(c) "}) 
for t in table:
    rows = t.find_all('tr')
    for row in rows:
        print(row.get_text())