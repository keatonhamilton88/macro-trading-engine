import numpy as np

def credit_sensor(prices):

    hyg = prices["HYG"]
    tlt = prices["TLT"]

    return np.log(hyg) - np.log(tlt)
