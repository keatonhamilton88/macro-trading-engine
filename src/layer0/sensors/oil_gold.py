import numpy as np

def inflation_sensor(prices):

    oil = prices["CL=F"]
    gold = prices["GC=F"]

    return np.log(oil) - np.log(gold)
