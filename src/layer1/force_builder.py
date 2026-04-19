import pandas as pd
from src.features.transforms import zscore_sensor


class ForceBuilder:

    FORCE_MAP = {

        "growth": [
            "hg_gc",
            "sox_spy",
            "ashr_spy",
            "eem_spy",
            "aud_jpy"
        ],

        "inflation": [
            "cl_gc",
            "hg_cl",
            "gc_si",
            "hg_tio"
        ],

        "risk": [
            "vix",
            "vix_vol",
            "vix_ratio",
            "gamma_strength",
            "spx_gex",
            "zero_dte_vol"
        ],

        "dollar": [
            "dx",
            "usd_cnh",
            "eur_usd",
            "usd_jpy",
            "eur_chf"
        ],

        "credit": [
            "hyg_tlt",
            "spy_tlt"
        ],

        "rates": [
            "zn_sr3",
            "zn_zt"
        ]
    }

    @staticmethod
    def build_forces(sensor_df):
        # 1. 'Fast' sensors from your Risk bucket
        FAST_SENSORS = ["vix", "vix_vol", "vix_ratio", "gamma_strength", "spx_gex", "zero_dte_vol"]
    
        # 2. COMPLETE list of all raw components used in your Ratios + Dollar force
        # If it's a standalone price or part of a ratio (like 'hg' in 'hg_gc'), it goes here.
        RAW_PRICE_TICKERS = [
            "DX-Y.NYB", "USDCNH=X", "EURUSD=X", "USDJPY=X", "EURCHF=X", # Dollar
            "SPY", "SOXX", "ASHR", "EEM", "TLT", "HYG",                 # Equities/Bonds
            "CL=F", "GC=F", "HG=F", "SI=F", "TIO=F",                    # Commodities
            "ZN=F", "ZT=F", "SR3=F", "AUDJPY=X"                         # Rates/Forex
        ]

    
        z_sensors = pd.DataFrame(index=sensor_df.index)
        normalized_fast = [s.lower() for s in FAST_SENSORS]
        normalized_prices = [t.lower() for t in RAW_PRICE_TICKERS]
    
        # 3. Apply Z-Score Logic
        for col in sensor_df.columns:
            col_lower = col.lower()
            
            # Check Lookback: Fast (20) vs Slow (252)
            lookback = 20 if col_lower in normalized_fast else 252
            
            # Check Type: Return (% change) vs Level (Ratio/Indicator)
            is_price = col_lower in normalized_prices
            
            z_sensors[col] = zscore_sensor(sensor_df[col], lookback, is_return=is_price)
    
        # 4. Filter for only the sensors defined in your FORCE_MAP
        forces = pd.DataFrame(index=z_sensors.index)
        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():
            # This aligns your processed z_sensors back to the 6 force names
            valid_sensors = [s for s in sensor_list if s in z_sensors.columns]
            if valid_sensors:
                forces[force_name] = z_sensors[valid_sensors].mean(axis=1, skipna=True)

        print(f"DEBUG: processed z_sensors columns: {z_sensors.columns.tolist()}")
        print(f"DEBUG: forces head: \n{forces.head()}")

        return forces.dropna(how='all').ffill().bfill()
