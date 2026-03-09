import numpy as np

def aud_jpy_sensor(prices):

    audjpy = prices["AUDJPY=X"]

    return np.log(audjpy)
