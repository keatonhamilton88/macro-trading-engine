import numpy as np

def gc_si(prices):

    gc = prices["GC=F"]
    si = prices["SI=F"]
  
    return np.log(gc) - np.log(si)
