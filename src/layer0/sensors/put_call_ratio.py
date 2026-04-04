import numpy as np
import pandas as pd

def put_call_ratio(prices):
    # 1. Safety Check: If prices is empty, return an empty Series
    if prices is None or prices.empty:
        return pd.Series(dtype=float)

    # 2. Placeholder: Currently returning 0.0 until you link your data source.
    # We name it 'pcr_signal' to remind us this is for conviction.
    pcr_signal = pd.Series(0.0, index=prices.index, name='pcr_signal')

    return pcr_signal


def put_call_conviction(prices, raw_pcr_data):
    """
    Standardizes the P/C ratio into a -1 to 1 conviction signal.
    High P/C (> 1.0) = Fear (Potentially Bullish Reversal)
    Low P/C (< 0.7) = Greed (Potentially Bearish Exhaustion)
    """
    # 1. Align the PCR data to your price dates
    pcr = raw_pcr_data.reindex(prices.index).ffill()
    
    # 2. Compare current PCR to its 20-day Moving Average
    pcr_ma = pcr.rolling(20).mean()
    
    # 3. Calculate distance from average (Standardizing)
    # This turns 'raw' data into a signal centered around 0
    conviction = (pcr - pcr_ma) / pcr_ma
    
    # 4. Use tanh to keep it between -1 and 1
    return np.tanh(conviction * 5) # Multiplying by 5 makes the signal 'snap' faster
