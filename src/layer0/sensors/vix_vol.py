import numpy as np
import pandas as pd

def vix_vol(prices):
    # 1. Safety Check: yfinance ticker is '^VVIX'
    if "^VVIX" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    # 2. Log Transform: Compresses the 'spikes' in VVIX
    # (VVIX can jump from 80 to 150; log makes this move more linear)
    vixvol = np.log(prices["^VVIX"].ffill())

    return vixvol.rename("vix_vol_log")

