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

