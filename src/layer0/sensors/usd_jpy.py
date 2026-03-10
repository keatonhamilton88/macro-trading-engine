def usd_jpy(prices):

    import numpy as np

    usdjpy = prices["JPY=X"]

    return np.log(usdjpy)
