import yfinance as yf
import pandas as pd
from sensors import vix, spx_gex, aud_jpy # Import your sensor functions
from ForceBuilder import ForceBuilder
from PCAEngine import PCAEngine
from HMMRegimeEngine import HMMRegimeEngine

def run_engine_test():
    # 1. DOWNLOAD DATA
    # Download at least 2 years for the 252-day PCA lookback
    tickers = ["SPY", "^VIX", "^VIX3M", "AUDJPY=X", "CL=F", "GC=F"]
    raw_data = yf.download(tickers, start="2022-01-01")['Close']
    raw_data = raw_data.ffill().dropna() 
    
    # 2. BUILD SENSORS
    # Create a dataframe where each column is one of your sensor outputs
    sensor_df = pd.DataFrame(index=raw_data.index)
    sensor_df['vix'] = vix(raw_data)
    sensor_df['aud_jpy'] = aud_jpy(raw_data)
    # ... add the rest of your 20+ sensors here
    
    # 3. BUILD FORCES (Layer 1)
    # This uses your Z-score logic and FORCE_MAP
    builder = ForceBuilder()
    forces = builder.build_forces(sensor_df)
    
    # 4. PCA DIMENSION REDUCTION
    pca = PCAEngine(n_components=3)
    pc_signals = pca.fit_transform(forces) # Learning the weights
    
    # 5. HMM REGIME DETECTION (Layer 2)
    hmm = HMMRegimeEngine(n_states=4)
    hmm.fit(pc_signals) # 'Learn' the market states
    
    # 6. OUTPUT RESULTS
    current_state = hmm.predict_states(pc_signals).iloc[-1]
    probs = hmm.predict_probabilities(pc_signals).iloc[-1]
    
    print(f"--- ENGINE TEST COMPLETE ---")
    print(f"Current Detected State: {current_state}")
    print(f"State Probabilities:\n{probs}")

if __name__ == "__main__":
    run_engine_test()

