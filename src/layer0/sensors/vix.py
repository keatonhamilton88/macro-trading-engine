def vix(prices):
    if not prices is None or prices.empty:
        return pd.Series(0.0, index=prices.index, name='vix')
    else:
        return pd.Series(dtype=float)

    return prices["^VIX"]
