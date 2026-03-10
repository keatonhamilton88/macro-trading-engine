import numpy as np

def eur_chf(prices):

    eurchf = prices["EURCHF=X"]

    return np.log(eurchf)
