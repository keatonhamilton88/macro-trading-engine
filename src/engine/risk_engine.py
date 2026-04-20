import numpy as np

class PositionSizer:
    def __init__(self, account_equity, risk_per_trade=0.01):
        self.account_equity = account_equity
        self.risk_per_trade = risk_per_trade
        # Multipliers for IBKR/CME contracts
        self.CONTRACT_SPECS = {
            "MES": 5, "MNQ": 2, "MBT": 0.1, "MET": 1.0, # Equities/Crypto
            "MGC": 10, "MCL": 100, "MNG": 500,           # Micro Commodities
            "ZS": 50, "KE": 50, "ZC": 50, "ZW": 50,      # Full-size Ags
            "6E": 125000, "ZN": 1000, "ZT": 2000         # FX and Rates
        }

    def get_quantity(self, ticker, atr, risk_multiple=2.0):
        """Calculates contract count based on ATR-defined risk."""
        if atr <= 0: return 0
        
        # 1. Total dollars we are willing to lose on this trade
        dollar_risk_cap = self.account_equity * self.risk_per_trade
        
        # 2. Points of 'breathing room' for the stop loss
        stop_points = atr * risk_multiple
        
        # 3. Dollar cost of that stop per 1 contract
        point_value = self.CONTRACT_SPECS.get(ticker, 1.0)
        cost_per_contract = stop_points * point_value
        
        # 4. Quantity (floor to stay under risk cap)
        quantity = int(np.floor(dollar_risk_cap / cost_per_contract))
        return max(0, quantity)

    def check_margin_capacity(self, current_excess_liquidity, proposed_initial_margin):
        """Prevents trade if it uses > 50% of remaining buffer."""
        buffer_limit = current_excess_liquidity * 0.5
        return proposed_initial_margin < buffer_limit
