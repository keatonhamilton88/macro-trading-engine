import pandas as pd
import yfinance as yf
import importlib
from src.layer1.force_builder import ForceBuilder # Import your blueprint

class SensorBuilder:
    def download_prices(self, tickers, start="2020-01-01"):
        # Download with multi_level_index=False to try and force a single level
        data = yf.download(tickers, start=start, multi_level_index=False)
        
        # If it still returns a MultiIndex (common with multiple tickers), flatten it manually
        if isinstance(data.columns, pd.MultiIndex):
            # This keeps 'Close', 'Open', etc. but drops the Ticker level
            data.columns = data.columns.get_level_values(0) 
            
        # Extract only the Close prices and align them
        prices = data[['Close']].ffill().dropna()
        
        # Final safety: rename columns to just the tickers if they are still 'Close'
        # For multiple tickers, yfinance often returns tickers as the columns under 'Close'
        if isinstance(data['Close'], pd.DataFrame):
            return data['Close'].ffill().dropna()
            
        return prices


    @staticmethod
    def get_col(df, name):
        # 1. Try exact match
        match = next((c for c in df.columns if c.upper() == name.upper()), None)
        if match: return match
        
        # 2. Try adding '=F' for Futures or '=X' for Forex if not found
        for suffix in ["=F", "=X", "^", "DX-Y.NYB"]:
            test_name = f"{name.upper()}{suffix}"
            match = next((c for c in df.columns if c.upper() == test_name), None)
            if match: return match
            
        return None



    def build_sensors(self, raw_prices):
        sensor_df = pd.DataFrame(index=raw_prices.index)
        
        # These contain underscores but are SINGLE-TICKER sensors
        SINGLE_ASSETS = ["aud_jpy", "vix_vol", "vix_ratio", "usd_cnh", "eur_usd", "usd_jpy", "eur_chf", "spx_gex"]
    
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



