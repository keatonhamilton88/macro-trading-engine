import yfinance as yf

class YFinanceLoader:

    def load_close(self, symbol, period="5y"):
        data = yf.download(symbol, period=period, auto_adjust=True)

        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs("Close", level=0, axis=1)
        
        return data
