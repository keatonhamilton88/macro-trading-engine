import yfinance as yf

class YFinanceLoader:

    def load_close(self, symbol, period="5y"):
        data = yf.download(symbol, period=period)
        return data['Close']
