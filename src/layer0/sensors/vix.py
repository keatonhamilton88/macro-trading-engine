import pandas as pd
import numpy as np

def vix(prices):
    # 1. Safety Check: If data is missing, return a blank Series
    if prices is None or "^VIX" not in prices:
        return pd.Series(index=prices.index if prices is not None else [], dtype=float)

    # 2. Return the actual VIX data
    # (Or return a Series of 0.0 if you are still just testing)
    return prices["^VIX"]

