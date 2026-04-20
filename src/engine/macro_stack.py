import pandas as pd
import numpy as np
from ib_insync import util

# Core Engine Imports
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.layer2.hmm_regime_engine import HMMRegimeEngine

def run_macro_stack(ib_connector):
    """
    The TWS-integrated pipeline.
    """
    # 1. Initialize your builders (Ensure these match your __init__ logic)
    sb = SensorBuilder()
    fb = ForceBuilder()

    # 2. DATA INGESTION (IBKR)
    # We use 'raw_prices' to stay consistent with your SensorBuilder.build_sensors(raw_prices)
    print("--- 📥 Fetching IBKR Institutional Data ---")
    raw_prices = ib_connector.get_all_toolbox_prices(lookback='2 Y')
    
    # 3. SENSOR CONSTRUCTION (Layer 0)
    print("--- 🛠 Building Sensors ---")
    sensor_df = sb.build_sensors(raw_prices)
    sensor_df = sensor_df.ffill().fillna(0) 
    
    # 4. FORCE AGGREGATION (Layer 1)
    print("--- 🌊 Aggregating Forces ---")
    forces = fb.build_forces(sensor_df)
    
    # 5. PCA & HMM (Layer 1.5 - 2)
    print("--- 🧠 Running PCA & HMM ---")
    pca = PCAEngine(n_components=3)
    pc_df = pca.fit_transform(forces)
    
    features = pd.concat([forces, pc_df], axis=1).dropna()
    hmm = HMMRegimeEngine(n_states=4)
    hmm.fit(features)
    
    # Returning a DICTIONARY is safer for the Monitor to unpack
    return {
        "forces": forces,
        "pc_df": pc_df,
        "hmm": hmm,
        "combined": features,
        "latest_date": forces.index[-1]
    }
