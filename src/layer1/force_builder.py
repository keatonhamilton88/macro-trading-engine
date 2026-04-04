import pandas as pd
from transforms import zscore_returns


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
            "vix_slope",
            "gamma_flip",
            "spx_gex"
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
    def build_forces(sensor_df, lookback=252):
        # 1. Define the 'Raw Currency/Price' list. 
        # Everything else in your map (ratios like hg_gc, levels like vix) is False.
        RAW_PRICE_TICKERS = [
            # Currencies (Dollar Force)
            "dx", "usd_cnh", "eur_usd", "usd_jpy", "eur_chf",
            
            # Raw Commodity Prices (used in Inflation/Growth calculations)
            "cl=f", "gc=f", "hg=f", "si=f", "tio=f", 
            
            # Equities & Bond Prices (used in Growth/Credit/Rates)
            "spy", "ashr", "eem", "sox", "hyg", "tlt", 
            "zn=f", "zt=f", "sr3=f"
]

    
        z_sensors = pd.DataFrame(index=sensor_df.index)
    
        # 2. Loop through every column and apply the specific Z-Score logic
        for col in sensor_df.columns:
            # If it's a raw currency, use % change. 
            # If it's a ratio (hg_gc) or level (vix/gex), use the raw level.
            use_return = col.lower() in [t.lower() for t in RAW_PRICE_TICKERS]
            
            z_sensors[col] = zscore_sensor(sensor_df[col], lookback, is_return=use_return)
    
        # 3. Clean up NaNs from the lookback window
        z_sensors = z_sensors.dropna(how='all')
    
        # 4. Map sensors into your 6 Market Forces
        forces = pd.DataFrame(index=z_sensors.index)
        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():
            valid_sensors = [s for s in sensor_list if s in z_sensors.columns]
            
            if len(valid_sensors) > 0:
                # We take the mean of the Z-scores to create the 'Force'
                forces[force_name] = z_sensors[valid_sensors].mean(axis=1)
    
        return forces

