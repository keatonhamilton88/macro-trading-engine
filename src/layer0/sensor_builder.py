import pandas as pd
import yfinance as yf
import importlib
from src.layer1.force_builder import ForceBuilder # Import your blueprint

class SensorBuilder:
    def download_prices(self, tickers, start="2010-01-01"):
        data = yf.download(tickers, start=start)["Close"]
        # Essential: Fill gaps and align holidays immediately
        return data.ffill().dropna()

    @staticmethod
    def get_col(df, name):
        """Universal case-insensitive column finder."""
        return next((c for c in df.columns if c.upper() == name.upper()), None)

    def build_sensors(self, raw_prices):
        sensor_df = pd.DataFrame(index=raw_prices.index)
        
        # We loop through the FORCE_MAP to see what we actually NEED to build
        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():
            for s_name in sensor_list:
                try:
                    # Dynamically find the file in your layer0 folder
                    module = importlib.import_module(f"src.layer0.sensors.{s_name}")
                    
                    # Define names that have underscores but are NOT ratios
                SINGLE_EXCEPTIONS = ["aud_jpy", "vix_vol", "vix_ratio", "usd_cnh", "eur_usd", "usd_jpy", "eur_chf", "spx_gex", "gamma_strength"]
                
                if "_" in s_name and s_name not in SINGLE_EXCEPTIONS:
                    # This is a REAL ratio (e.g., ashr_spy)
                    t1, t2 = s_name.split("_")
                    c1, c2 = self.get_col(raw_prices, t1), self.get_col(raw_prices, t2)
                    sensor_df[s_name] = module.compute(raw_prices, c1, c2)
                else:
                    # This is a SINGLE asset (even if it has an underscore like aud_jpy)
                    c1 = self.get_col(raw_prices, s_name)
                    sensor_df[s_name] = module.compute(raw_prices, c1)

                        
                except Exception as e:
                    print(f"⚠️ Warning: Could not build {s_name}: {e}")
                    sensor_df[s_name] = pd.Series(0.0, index=raw_prices.index)

        return sensor_df

