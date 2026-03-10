import pandas as pd
import yfinance as yf

from layer0.sensor_registry import SENSOR_REGISTRY

class SensorBuilder:

    def download_prices(self, tickers, start="2010-01-01"):

        data = yf.download(tickers, start=start)["Close"]

        if isinstance(data, pd.Series):
            data = data.to_frame()

        return data


    def build_sensors(self, prices):

        sensors = pd.DataFrame(index=prices.index)

        for name, fn in SENSOR_REGISTRY.items():

            sensors[name] = fn(prices)

        return sensors.dropna()
