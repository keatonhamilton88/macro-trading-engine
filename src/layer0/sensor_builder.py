import pandas as pd
import yfinance as yf
import importlib
from src.layer1.force_builder import ForceBuilder # Import your blueprint

class SensorBuilder:
    def download_prices(self, tickers, start="2020-01-01"):
        # 1. Force the most recent yfinance version to drop the multi-index if possible
        data = yf.download(tickers, start=start, multi_level_index=False)
        
        # 2. Extract 'Close' - if MultiIndex persists, flatten it manually
        if isinstance(data.columns, pd.MultiIndex):
            # We only want the 'Ticker' level from the 'Close' group
            if 'Close' in data.columns.levels[0]:
                data = data['Close']
            else:
                # Fallback: flatten (Price, Ticker) to just (Ticker)
                data.columns = data.columns.get_level_values(1)
                
        # 3. Final alignment and gap filling
        return data.ffill().dropna()


    @staticmethod
    def get_col(df, name):
        cols = [str(c).upper() for c in df.columns]
        target = name.upper()
        
        # Check exact match
        if target in cols:
            return df.columns[cols.index(target)]
        
        # Check yfinance specific variations
        variations = [f"{target}=F", f"{target}=X", f"^{target}", "DX-Y.NYB"]
        for v in variations:
            if v in cols:
                return df.columns[cols.index(v)]
        return None




    def build_sensors(self, raw_prices):
        sensor_df = pd.DataFrame(index=raw_prices.index)
        
        # These contain underscores but are SINGLE-TICKER sensors
        SINGLE_ASSETS = ["aud_jpy", "vix_vol", "vix_ratio", "usd_cnh", "eur_usd", "usd_jpy", "eur_chf", "spx_gex", "zero_dte_vol"]
    
        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():
            for s_name in sensor_list:
                try:
                    module = importlib.import_module(f"src.layer0.sensors.{s_name}")
                    
                    # Only split if it has an underscore AND isn't in our 'Single' list
                    if "_" in s_name and s_name not in SINGLE_ASSETS:
                        t1, t2 = s_name.split("_")
                        c1, c2 = self.get_col(raw_prices, t1), self.get_col(raw_prices, t2)
                        sensor_df[s_name] = module.compute(raw_prices, c1, c2)
                    else:
                        c1 = self.get_col(raw_prices, s_name)
                        sensor_df[s_name] = module.compute(raw_prices, c1)
                        
                except Exception as e:
                    print(f"⚠️ Sensor Build Failed: {s_name} | {e}")
                    sensor_df[s_name] = pd.Series(0.0, index=raw_prices.index)
                    
        return sensor_df



