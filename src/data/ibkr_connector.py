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

    def get_macro_appropriate_contract(self, symbol, min_dte=20):
        """
        Ensures we aren't buying a 'dying' contract.
        If front month < 20 days left, grab the next one.
        """
        contracts = self.ib.reqContractDetails(Future(symbol))
        # Filter and sort by expiry
        valid_contracts = [c.summary for c in contracts if c.summary.lastTradeDateOrContractMonth > threshold_date]
        return valid_contracts[0] # Returns the first contract that meets our time horizon


# Example Contract Definitions for your Toolbox
# Micro Gold: MGC @ NYMEX
# Micro Bitcoin: MBT @ CME
# FX Cash: EUR.USD @ IDEALPRO
