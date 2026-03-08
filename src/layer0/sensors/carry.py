import numpy as np

def carry_sensor(prices):

    audjpy = prices["AUDJPY=X"]

    return np.log(audjpy)
