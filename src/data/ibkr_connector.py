from ib_insync import *
import pandas as pd

class IBKRConnector:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id

    def connect(self):
        if not self.ib.isConnected():
            self.ib.connect(self.host, self.port, clientId=self.client_id)

    def get_historical_data(self, contract, duration='1 Y', bar_size='1 day'):
        """Fetches institutional-grade bars for ATR and Sensors."""
        self.connect()
        bars = self.ib.reqHistoricalData(
            contract, endDateTime='', durationStr=duration,
            barSizeSetting=bar_size, whatToShow='TRADES', useRTH=True
        )
        df = util.df(bars)
        if df is not None:
            df.set_index('date', inplace=True)
        return df

# Example Contract Definitions for your Toolbox
# Micro Gold: MGC @ NYMEX
# Micro Bitcoin: MBT @ CME
# FX Cash: EUR.USD @ IDEALPRO
