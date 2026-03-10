import numpy as np

def oil_gold(prices):

    oil = prices["CL=F"]
    gold = prices["GC=F"]

    return np.log(oil) - np.log(gold)
