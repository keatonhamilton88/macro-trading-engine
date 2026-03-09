def usd_jpy_sensor(prices):

    import numpy as np

    usdjpy = prices["USDJPY=X"]

    return np.log(usdjpy)
