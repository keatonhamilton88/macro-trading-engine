import numpy as np

def aud_jpy(prices):

    audjpy = prices["AUDJPY=X"]

    return np.log(audjpy)
