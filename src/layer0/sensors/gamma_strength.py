# In gamma_strength.py
def compute(prices, price_col, flip_col):
    if price_col is None or flip_col is None:
        return pd.Series(index=prices.index, dtype=float)
    
    dist = (prices[price_col] - prices[flip_col]) / prices[flip_col]
    return np.tanh(dist / 0.02) # Our 'Soft' signal




