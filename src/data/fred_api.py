from fredapi import Fred

class FredLoader:
    def __init__(self, api_key):
        self.fred = Fred(api_key=api_key)

    def get_macro_liquidity(self):
        # WALCL is the Fed Balance Sheet
        return self.fred.get_series('WALCL')
