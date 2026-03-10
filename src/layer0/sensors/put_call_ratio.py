import numpy as np
import pandas as pd 

def put_call_ratio(prices):    
     if not prices.empty:
            return pd.Series(0.0, index=prices.index, name='put_call_ratio')
     else:
       return pd.Series(dtype=float)
