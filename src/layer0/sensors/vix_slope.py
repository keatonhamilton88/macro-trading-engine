import numpy as np

def vix_slope_sensor(prices):
  
    return prices["VIX3M"] - prices["^VIX"]
