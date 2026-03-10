def vix_vol(prices):

    vixvol = prices["VVIX"]

    return np.log(vixvol)
