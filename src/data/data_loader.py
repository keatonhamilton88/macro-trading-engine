import yfinance as yf
import pandas as pd

class YFinanceLoader:

    def load_close(self, symbol, period="5y"):
        data = yf.download(symbol, period=period, auto_adjust=True)

        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs("Close", level=0, axis=1)
        
        return data


    def get_last_valid_trading_date(df):
    """Finds the most recent row that isn't all zeros/NaNs."""
    # Drop rows where everything is 0.0 (our fillna result)
    clean_df = df[(df != 0).any(axis=1)]
    if clean_df.empty:
        return None
    return clean_df.index[-1]

    # In run_engine.py after build_forces:
    valid_date = get_last_valid_trading_date(forces)
    if valid_date:
        print(f"📅 Last Valid Trading Day: {valid_date.date()}")
        # If you want to force the PCA to only care about real data:
        forces = forces.loc[:valid_date] 

