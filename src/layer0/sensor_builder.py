import yfinance as yf
import pandas as pd


class SensorBuilder:

    def download_prices(self, tickers, start="2010-01-01"):

        data = yf.download(tickers, start=start)["Close"]

        if isinstance(data, pd.Series):
            data = data.to_frame()

        return data


    def build_sensors(self, prices):

        sensors = pd.DataFrame(index=prices.index)

        # Growth sensor
        sensors["growth"] = prices["HG=F"] / prices["GC=F"]

        # Inflation sensor
        sensors["inflation"] = prices["CL=F"] / prices["GC=F"]

        # Risk appetite
        sensors["risk"] = prices["SPY"] / prices["TLT"]

        # Credit stress
        sensors["credit"] = prices["HYG"] / prices["LQD"]

        # EM stress
        sensors["em"] = prices["EEM"] / prices["SPY"]

        # Carry proxy
        sensors["carry"] = prices["AUDJPY=X"]

        # Dollar strength
        sensors["dollar"] = prices["DX-Y.NYB"]

        # Volatility
        sensors["volatility"] = prices["^VIX"]

        return sensors.dropna()
