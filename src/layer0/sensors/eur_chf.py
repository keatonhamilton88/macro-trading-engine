import numpy as np

def eur_chf_sensor(prices):

    eurchf = prices["EURCHF=X"]

    return np.log(eurchf)
