import pandas as pd
import numpy as np

def vix(prices):
    # This finds "^VIX", "^vix", or "VIX" automatically
    ticker = next((c for c in prices.columns if c.upper() == "^VIX"), None)
    
    if prices is None or ticker is None:
        return pd.Series(index=prices.index if prices is not None else [], dtype=float)

    return prices[ticker]


