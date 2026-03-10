import numpy as np

def copper_iron(prices):

    hg = prices["HG=F"]
    tio = prices["TIO=F"]

    return np.log(hg) - np.log(tio)
