# import numpy as np
# import pandas as pd

# def compute(prices, col1=None):
#     # If you have no raw data yet, return 0.0
#     if col1 is None:
#         return pd.Series(0.0, index=prices.index)
    
#     # Once you link data, the 'conviction' math goes here
#     raw_pcr = prices[col1].ffill()
#     pcr_ma = raw_pcr.rolling(20).mean()
#     conviction = (raw_pcr - pcr_ma) / (pcr_ma + 1e-8)
#     return np.tanh(conviction * 5)

import pandas as pd
import numpy as np

def compute(prices, col1=None):
    # Mock data: random noise around 0 so PCA can calculate variance
    # This prevents the 'Singular Matrix' error in the PCAEngine
    mock_values = np.random.normal(0, 0.01, size=len(prices))
    return pd.Series(mock_values, index=prices.index)


