import numpy as np

def hyg_tlt(prices):

    hyg = prices["HYG"]
    tlt = prices["TLT"]

    return np.log(hyg) - np.log(tlt)
