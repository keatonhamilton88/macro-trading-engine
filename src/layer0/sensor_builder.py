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
        sensors["growth_sensor"] = prices["HG=F"] / prices["GC=F"]

        # Inflation sensor
        sensors["inflation_sensor"] = prices["CL=F"] / prices["GC=F"]

        # Risk appetite
        sensors["risk_sensor"] = prices["SPY"] / prices["TLT"]

        # Credit stress
        sensors["credit_sensor"] = prices["HYG"] / prices["LQD"]

        # EM stress
        sensors["em_sensor"] = prices["EEM"] / prices["SPY"]

        # Carry proxy
        sensors["carry_sensor"] = prices["AUDJPY=X"]

        # Dollar strength
        sensors["dollar_sensor"] = prices["DX-Y.NYB"]

        # Volatility
        sensors["vol_sensor"] = prices["^VIX"]

        return sensors.dropna()
