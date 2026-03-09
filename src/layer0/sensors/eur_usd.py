def eur_usd_sensor(prices):

    import numpy as np

    eurusd = prices["EURUSD=X"]

    return np.log(eurusd)
