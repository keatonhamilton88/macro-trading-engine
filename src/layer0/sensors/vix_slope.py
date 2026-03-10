import numpy as np

def vix_slope(prices):
  
    return prices["VIX3M"] - prices["^VIX"]
