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


#  Integration Tip for PCA
# try passing two versions of VVIX to the PCA:
# The Level: np.log(VVIX) (captures the current "Fear Regime").
# The Momentum: VVIX.pct_change() (captures the "Sudden Panic"). 
# This allows the PCA to distinguish between a market that is consistently volatile (like a bear market) and a market that just suffered a sudden shock. 


