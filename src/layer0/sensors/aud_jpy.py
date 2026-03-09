import numpy as np

def audjpy_sensor(prices):

    audjpy = prices["AUDJPY=X"]

    return np.log(audjpy)
