def usd_jpy(prices):

    import numpy as np

    usdjpy = prices["USDJPY=X"]

    return np.log(usdjpy)
