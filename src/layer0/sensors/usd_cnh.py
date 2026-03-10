import numpy as np

def usd_cnh(prices):

    usdcnh = prices["USDCNH=X"]

    return np.log(usdcnh)
