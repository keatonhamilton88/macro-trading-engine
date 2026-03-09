def sox_spy_sensor(prices):

    import numpy as np

    sox = prices["SOXX"]
    spy = prices["SPY"]

    return np.log(sox) - np.log(spy)
