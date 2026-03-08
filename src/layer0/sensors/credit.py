import numpy as np

def credit_sensor(prices):

    hyg = prices["HYG"]
    lqd = prices["LQD"]

    return np.log(hyg) - np.log(lqd)
