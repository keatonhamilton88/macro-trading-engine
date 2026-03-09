import numpy as np

def oil_gold_sensor(prices):

    oil = prices["CL=F"]
    gold = prices["GC=F"]

    return np.log(oil) - np.log(gold)
