import numpy as np

def usd_cnh(prices):

    usdcnh = prices["CNY=X"]

    return np.log(usdcnh)
