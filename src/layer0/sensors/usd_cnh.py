import numpy as np

def usd_cnh_sensor(prices):

    usdcnh = prices["USDCNH=X"]

    return np.log(usdcnh)
