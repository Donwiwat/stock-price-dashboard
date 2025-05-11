import yfinance as yf

def retrieve_financials(symbol: str):
    #financials_dict = dict()
    # financials_dict[ticker] = yf.Ticker(ticker).financials
    # return financials_dict
    return yf.Ticker(symbol).financials

def retrieve_balance_sheet(symbol: str):
    ticker = yf.Ticker(symbol)
    return ticker.balancesheet

def retrieve_cashflow(symbol: str):
    ticker = yf.Ticker(symbol)
    return ticker.cashflow

if __name__ == "__main__":
    print(retrieve_financials('mbk.bk'))
# mbk = yf.Ticker('mbk.bk')

# interval = '1d'
# start = '2022-1-1'
# end = '2022-11-23'

# mbk_price_df = mbk.history(interval='1d',start=start,end=end)
# mbk_price_df.to_csv('test.csv')

# print(mbk.financials)
# print(mbk.balancesheet)
# print(mbk.cashflow)