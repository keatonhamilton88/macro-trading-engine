import pandas as pd
import numpy as np
from ib_insync import util

# Core Engine Imports
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.layer2.hmm_regime_engine import HMMRegimeEngine

def run_macro_stack(ib_connector, sensor_builder, force_builder):
    """
    The 'Golden Path' from IBKR Raw Data to Macro Signals.
    """
    # 1. DATA INGESTION (IBKR)
    # Swapping yfinance for the TWS API loader
    raw_data = ib_connector.get_all_toolbox_prices(lookback='2 Y')
    
    # 2. SENSOR CONSTRUCTION (Layer 0)
    # Computes your 23+ custom sensors (aud_jpy, hg_gc, etc.)
    sensor_df = sensor_builder.build_sensors(raw_data)
    sensor_df = sensor_df.ffill().fillna(0) # Standardize holes
    
    # 3. FORCE AGGREGATION (Layer 1)
    # Applies 'Fast' and 'Slow' Z-scores to create the 6 Forces
    forces = force_builder.build_forces(sensor_df)
    
    # 4. DIMENSION REDUCTION (Layer 1.5)
    # PCA extracts the 3 main Market Forces (Beta, Risk, Rotation)
    pca = PCAEngine(n_components=3)
    pc_df = pca.fit_transform(forces)
    
    # 5. REGIME CLASSIFICATION (Layer 2)
    # Combined features for the HMM
    features = pd.concat([forces, pc_df], axis=1).dropna()
    hmm = HMMRegimeEngine(n_states=4)
    hmm.fit(features)
    
    return {
        "forces": forces,
        "pca": pc_df,
        "hmm": hmm,
        "features": features,
        "latest_date": forces.index[-1]
    }
