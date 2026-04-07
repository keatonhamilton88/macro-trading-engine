import pandas as pd
import yfinance as yf
import importlib
from src.layer1.force_builder import ForceBuilder # Import your blueprint

class SensorBuilder:
    def download_prices(self, tickers, start="2020-01-01"):
        # 1. Download all tickers at once
        data = yf.download(tickers, start=start)
        
        # 2. Extract only the 'Close' prices
        if 'Close' in data.columns:
            prices = data['Close']
        else:
            prices = data
            
        # 3. Clean and Align: ffill handles holidays, dropna ensures a clean start
        return prices.ffill().dropna()

    @staticmethod
    def get_col(df, name):
        """Finds a column name regardless of case (e.g., 'SPY' vs 'spy')."""
        return next((c for c in df.columns if c.upper() == name.upper()), None)


        def build_sensors(self, raw_prices):
        sensor_df = pd.DataFrame(index=raw_prices.index)
        
        # Names with underscores that are SINGLE assets
        SINGLE_EXCEPTIONS = ["aud_jpy", "vix_vol", "vix_ratio", "usd_cnh", "eur_usd", "usd_jpy", "eur_chf", "spx_gex", "gamma_strength"]

        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():
            for s_name in sensor_list:
                try:
                    module = importlib.import_module(f"src.layer0.sensors.{s_name}")
                    
                    # Logic: If it has an underscore AND it's not a single exception -> It's a Ratio
                    if "_" in s_name and s_name not in SINGLE_EXCEPTIONS:
                        parts = s_name.split("_")
                        t1, t2 = parts[0], parts[1] # Safe split
                        c1, c2 = self.get_col(raw_prices, t1), self.get_col(raw_prices, t2)
                        sensor_df[s_name] = module.compute(raw_prices, c1, c2)
                    else:
                        # It's a Single asset
                        c1 = self.get_col(raw_prices, s_name)
                        sensor_df[s_name] = module.compute(raw_prices, c1)
                        
                except Exception as e:
                    print(f"Could not build sensor {s_name}: {e}")
                    sensor_df[s_name] = pd.Series(0.0, index=raw_prices.index)
                    
        return sensor_df


