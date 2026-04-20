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


    def validate_and_size(self, ticker, atr, current_excess_liq, initial_margin_req):
        """
        Unified logic: Sizes by ATR, then kills the trade if it violates 
        either the 10% per-trade cap or your 30% account buffer.
        """
        # 1. Calculate Quantity based on ATR
        dollar_risk_cap = self.account_equity * self.risk_per_trade
        stop_points = atr * 2.0 
        point_value = self.CONTRACT_SPECS.get(ticker, 1.0)
        cost_per_contract = stop_points * point_value
        quantity = int(np.floor(dollar_risk_cap / cost_per_contract))
    
        # 2. Check PER-TRADE Margin Ceiling (e.g., 10% of liquidity)
        per_trade_cap = self.account_equity * 0.10
        if initial_margin_req > per_trade_cap:
            print(f"⚠️ {ticker} rejected: Margin requirement exceeds 10% per-trade cap.")
            return 0
    
        # 3. Check TOTAL ACCOUNT Buffer (Your 30% Rule)
        # If the new trade leaves you with < 30% Excess Liquidity, reject it.
        if (current_excess_liq - initial_margin_req) < (self.account_equity * 0.30):
            print(f"⚠️ {ticker} rejected: Violates your 30% Account Margin Buffer.")
            return 0
    
        return quantity

