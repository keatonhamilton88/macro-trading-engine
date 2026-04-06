import pandas as pd
import yfinance as yf
import importlib
from layer1.ForceBuilder import ForceBuilder # Import your blueprint

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
                    module = importlib.import_module(f"layer0.{s_name}")
                    
                    if "_" in s_name:
                        # RATIO: Find two parts (e.g. 'hg' and 'gc')
                        t1, t2 = s_name.split("_")
                        c1, c2 = self.get_col(raw_prices, t1), self.get_col(raw_prices, t2)
                        sensor_df[s_name] = module.compute(raw_prices, c1, c2)
                    else:
                        # SINGLE: Find one part (e.g. 'vix')
                        c1 = self.get_col(raw_prices, s_name)
                        sensor_df[s_name] = module.compute(raw_prices, c1)
                        
                except Exception as e:
                    print(f"⚠️ Warning: Could not build {s_name}: {e}")
                    sensor_df[s_name] = pd.Series(0.0, index=raw_prices.index)

        return sensor_df

