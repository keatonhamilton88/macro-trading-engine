import numpy as np

def credit_sensor(prices):

    hyg = prices["HYG"]
    lqd = prices["TLT"]

    return np.log(hyg) - np.log(tlt)
