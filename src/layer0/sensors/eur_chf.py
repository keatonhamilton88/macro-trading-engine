import numpy as np

def eur_chf_sensor(prices):

    eurchf = prices["EUR_CHF"]

    return np.log(eurchf)
