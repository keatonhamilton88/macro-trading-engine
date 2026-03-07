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
        sensors["growth_sensors"] = prices["HG=F"] / prices["GC=F"]

        # Inflation sensor
        sensors["inflation_sensors"] = prices["CL=F"] / prices["GC=F"]

        # Risk appetite
        sensors["risk_sensors"] = prices["SPY"] / prices["TLT"]

        # Credit stress
        sensors["credit_sensors"] = prices["HYG"] / prices["LQD"]

        # EM stress
        sensors["em_sensors"] = prices["EEM"] / prices["SPY"]

        # Carry proxy
        sensors["carry_sensors"] = prices["AUDJPY=X"]

        # Dollar strength
        sensors["dollar_sensors"] = prices["DX-Y.NYB"]

        # Volatility
        sensors["volatility_sensors"] = prices["^VIX"]

        return sensors.dropna()
