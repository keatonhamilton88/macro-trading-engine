import pandas as pd
import yfinance as yf
import importlib
from src.layer1.force_builder import ForceBuilder # Import your blueprint

class SensorBuilder:
    def download_prices(self, tickers, start="2020-01-01"):
        # 1. Download raw data
        data = yf.download(tickers, start=start, group_by='column')
        
        # 2. Extract only Close prices
        # This handles the most common yfinance MultiIndex structures
        if isinstance(data.columns, pd.MultiIndex):
            if 'Close' in data.columns.levels[0]:
                prices = data['Close']
            else:
                # Fallback if 'Close' is at a different level
                prices = data.xs('Close', axis=1, level=0, drop_level=True)
        else:
            prices = data
        
        # 3. Align and fill gaps (Holidays/Timezones)
        return prices.ffill().dropna()

    @staticmethod
    def get_col(df, name):
        # This is the "Translator" that connects your Force Map to yfinance
        cols = [str(c).upper() for c in df.columns]
        search_target = name.upper()
    
        # Exact Match
        if search_target in cols:
            return df.columns[cols.index(search_target)]
    
        # Smart Suffix Match (cl -> CL=F, vix -> ^VIX)
        suffixes = ["=F", "=X", "^", "DX-Y.NYB"]
        for s in suffixes:
            test = f"{search_target}{s}" if s != "^" else f"^{search_target}"
            if test in cols:
                return df.columns[cols.index(test)]
    
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



