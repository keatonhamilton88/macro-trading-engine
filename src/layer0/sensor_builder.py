import pandas as pd
import importlib
from ib_insync import util
from src.layer1.force_builder import ForceBuilder

class SensorBuilder:
    def __init__(self, ib_connector=None):
        self.ib_connector = ib_connector

    def download_prices(self, tickers=None, start=None):
        """
        Switched to IBKR: Fetches institutional-grade data.
        Note: 'tickers' and 'start' are handled by the ib_connector 
        logic to ensure contract qualification.
        """
        if self.ib_connector is None:
            raise ValueError("IBKRConnector instance required for price downloads.")
            
        # The connector will return a cleaned, aligned DataFrame (raw_prices)
        # formatted specifically for our sensor logic.
        data = self.ib_connector.get_all_toolbox_prices(duration='2 Y')
        
        # Ensure column names are clean upper-case strings
        data.columns = [str(c).upper() for c in data.columns]
        return data.ffill().dropna()

    @staticmethod
    def get_col(df, name):
        """
        Updated for IBKR: No more '^' or '=F' suffix issues.
        The connector maps 'MGC' to 'MGC' directly.
        """
        cols = [str(c).upper() for c in df.columns]
        target = name.upper()
        
        if target in cols:
            return df.columns[cols.index(target)]
        
        # Fallback for common IBKR vs. Internal naming mismatches
        variations = [f"{target}", f"{target}USD", f"USD{target}"]
        for v in variations:
            if v in cols:
                return df.columns[cols.index(v)]
        return None

    def build_sensors(self, raw_prices):
        sensor_df = pd.DataFrame(index=raw_prices.index)
        
        # SINGLE-TICKER sensors (preventing underscore-split logic)
        SINGLE_ASSETS = [
            "aud_jpy", "vix_vol", "vix_ratio", "usd_cnh", "eur_usd", 
            "usd_jpy", "eur_chf", "spx_gex", "zero_dte_vol", "vix"
        ]
    
        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():
            for s_name in sensor_list:
                try:
                    module = importlib.import_module(f"src.layer0.sensors.{s_name}")
                    
                    if "_" in s_name and s_name not in SINGLE_ASSETS:
                        t1, t2 = s_name.split("_")
                        c1, c2 = self.get_col(raw_prices, t1), self.get_col(raw_prices, t2)
                        sensor_df[s_name] = module.compute(raw_prices, c1, c2)
                    else:
                        c1 = self.get_col(raw_prices, s_name)
                        sensor_df[s_name] = module.compute(raw_prices, c1)
                        
                except Exception as e:
                    # In production, we log this and return 0.0 to prevent PCA failure
                    print(f"⚠️ Sensor Build Failed: {s_name} | {e}")
                    sensor_df[s_name] = pd.Series(0.0, index=raw_prices.index)
                    
        return sensor_df




