def eur_usd(prices):

    import numpy as np

    eurusd = prices["EURUSD=X"]

    return np.log(eurusd)
