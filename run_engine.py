import pandas as pd
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.data.data_loader import YFinanceLoader # Will swap to IBKRLoader later

def run_trading_engine():
    # 1. Initialize
    builder = SensorBuilder()
    
    # Define Tickers (Ensure these match your ForceBuilder.RAW_PRICE_TICKERS)
    tickers = [
        "SPY", "TLT", "HYG", "GLD", "SLV", "^VIX", "DX-Y.NYB", 
        "CL=F", "GC=F", "HG=F", "ZN=F", "ZT=F", "AUDJPY=X"
    ]
    
    # 2. Download Data (Need 1 year+ for Slow Z-scores)
    print("--- 📥 Downloading Market Data ---")
    prices = builder.download_prices(tickers, start="2022-01-01")
    
    # IMPORTANT: Add the mock column for the Gamma Sensor to prevent NaNs
    prices['SPX_GEX_FLIP'] = 5000.0 
    
    # 3. Build Sensors (Layer 0)
    print("--- 🛠 Building Sensors (Layer 0) ---")
    sensors = builder.build_sensors(prices)
    
    # 4. Build Forces (Layer 1)
    print("--- 🌊 Aggregating Market Forces (Layer 1) ---")
    # Calling the class method directly
    forces = ForceBuilder.build_forces(sensors)
    
    if forces.empty or len(forces) < 100:
        print(f"❌ Error: Insufficient Force Data. Count: {len(forces)}")
        return

    # 5. PCA Engine (Layer 1.5)
    # We pass 'forces' (the whole history) so it can find variance
    print("--- 🔬 Running PCA Engine ---")
    pca = PCAEngine(n_components=3)
    pc_df = pca.fit_transform(forces) 
    
    # 6. Extract Latest Signal for Reporting
    # Use your new Data Loader function to find the last 'real' data point
    from src.data.data_loader import get_last_valid_trading_date
    valid_date = get_last_valid_trading_date(forces)
    
    if valid_date:
        print(f"📅 Report for Date: {valid_date.date()}")
        f_today = forces.loc[valid_date]
        p_today = pc_df.loc[valid_date]
        
        print(f"✅ PCA Success | PC1 (Beta): {p_today['PC1']:.2f}")
        print(f"Current Forces: Growth: {f_today['growth']:.2f} | Risk: {f_today['risk']:.2f}")
    else:
        print("❌ No valid trading data found in the current window.")

    if valid_date:
        print(f"📅 Report for Date: {valid_date.date()}")

        # HMM REGIME DETECTION 
        # --- 🧠 Detecting Market Regimes (Layer 2) ---
        print("--- 🧠 Detecting Market Regimes (Layer 2) ---")
        combined_features = pd.concat([forces, pc_df], axis=1).dropna().copy()
        
        hmm = HMMRegimeEngine(n_states=4)
        hmm.fit(combined_features)
        
        # Use the valid_date to ensure we aren't looking at "future" empty rows
        current_state = hmm.predict_states(combined_features).loc[valid_date]
        probs = hmm.predict_probabilities(combined_features).loc[valid_date]
        
        # --- 6. OUTPUT & DIAGNOSTICS ---
        print("\n" + "="*30)
        print(f"🚀 ENGINE STATUS: OPERATIONAL")
        print(f"📍 CURRENT STATE: {current_state}")
        print(f"📊 CONFIDENCE: {probs.max():.2%}")
        print("="*30)

        # ... (Transition Matrix and Loadings code here) ...

        # --- 7. REGIME CLASSIFICATION (The Final Label) ---
        scores = RegimeEngine.compute_scores(forces)
        regime, confidence = RegimeEngine.classify(scores)
        
        print(f"\nFinal Regime Logic Label: {regime.loc[valid_date]}")
        print(f"Regime Logic Confidence: {confidence.loc[valid_date]:.2f}")

    else:
        print("❌ No valid trading data found in the current window.")

if __name__ == "__main__":
    run_trading_engine()


# import yfinance as yf
# import pandas as pd
# from sensors import vix, spx_gex, aud_jpy # Import your sensor functions
# from ForceBuilder import ForceBuilder
# from PCAEngine import PCAEngine
# from HMMRegimeEngine import HMMRegimeEngine

# def run_engine_test():
#     # 1. DOWNLOAD DATA
#     # Download at least 2 years for the 252-day PCA lookback
#     tickers = ["SPY", "^VIX", "^VIX3M", "AUDJPY=X", "CL=F", "GC=F"]
#     raw_data = yf.download(tickers, start="2022-01-01")['Close']
#     raw_data = raw_data.ffill().dropna() 
    
#     # 2. BUILD SENSORS
#     # Create a dataframe where each column is one of your sensor outputs
#     sensor_df = pd.DataFrame(index=raw_data.index)
#     sensor_df['vix'] = vix(raw_data)
#     sensor_df['aud_jpy'] = aud_jpy(raw_data)
#     # ... add the rest of your 20+ sensors here
    
#     # 3. BUILD FORCES (Layer 1)
#     # This uses your Z-score logic and FORCE_MAP
#     builder = ForceBuilder()
#     forces = builder.build_forces(sensor_df)
    
#     # 4. PCA DIMENSION REDUCTION
#     pca = PCAEngine(n_components=3)
#     pc_signals = pca.fit_transform(forces) # Learning the weights
    
#     # 5. HMM REGIME DETECTION (Layer 2)
#     hmm = HMMRegimeEngine(n_states=4)
#     hmm.fit(pc_signals) # 'Learn' the market states
    
#     # 6. OUTPUT RESULTS
#     current_state = hmm.predict_states(pc_signals).iloc[-1]
#     probs = hmm.predict_probabilities(pc_signals).iloc[-1]
    
#     print(f"--- ENGINE TEST COMPLETE ---")
#     print(f"Current Detected State: {current_state}")
#     print(f"State Probabilities:\n{probs}")

# if __name__ == "__main__":
#     run_engine_test()

