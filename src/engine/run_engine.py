import pandas as pd
import yfinance as yf
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.layer2.hmm_regime_engine import HMMRegimeEngine
from src.layer2.regime_engine import RegimeEngine

def run_trading_engine():
    # -----------------------------------
    # 1. SETUP & DATA DOWNLOAD
    # -----------------------------------
    builder = SensorBuilder()
    
    # Complete Ticker List for all 6 Market Forces
    tickers = [
        "HG=F", "TIO=F", "GC=F", "CL=F", "SI=F",        # Inflation / Growth
        "SOXX", "SPY", "ASHR", "EEM", "FXI",            # Growth / Equity
        "AUDJPY=X", "TLT", "HYG",                       # Credit / Growth
        "^VIX", "^VVIX", "^VIX3M",                      # Risk (Volatility)
        "DX-Y.NYB", "USDCNH=X", "USDJPY=X", "EURUSD=X", # Dollar
        "EURCHF=X", "ZN=F", "SR3=F", "ZT=F"             # Rates / Credit
    ]

    print("--- 📥 Downloading Market Data ---")
    # Using 2020 to give plenty of 'warm-up' for the 252-day Z-scores
    prices = builder.download_prices(tickers, start="2020-01-01")
    
    # -----------------------------------
    # 2. BUILD SENSORS (Layer 0)
    # -----------------------------------
    print("--- 🛠 Building Sensors (Layer 0) ---")
    # This uses the dynamic importlib loop we built
    sensors = builder.build_sensors(prices)
    
    # -----------------------------------
    # 3. BUILD MACRO FORCES (Layer 1)
    # -----------------------------------
    print("--- 🌊 Aggregating Market Forces (Layer 1) ---")
    # This applies the 'Fast' and 'Slow' Z-scores
    forces = ForceBuilder.build_forces(sensors)
    
    if forces.empty:
        print("❌ Error: ForceBuilder returned empty data. Check your Z-score lookbacks.")
        return

    # -----------------------------------
    # 4. PCA OVERLAY (Dimension Reduction)
    # -----------------------------------
    print("--- 🔬 Running PCA Engine ---")
    pca = PCAEngine(n_components=3)
    # PCA runs on the 6 'Forces', not the 27 raw sensors
    pc_df = pca.fit_transform(forces)

    # --- THE BRIDGE ---
    combined = pd.concat([forces, pc_df], axis=1).dropna()
    
    # -----------------------------------
    # 5. HMM REGIME DETECTION (Layer 2)
    # -----------------------------------
    print("--- 🧠 Detecting Market Regimes (Layer 2) ---")
    combined_features = pd.concat([forces, pc_df], axis=1).dropna()
    
    hmm = HMMRegimeEngine(n_states=4)
    hmm.fit(combined_features)
    
    current_state = hmm.predict_states(combined_features).iloc[-1]
    probs = hmm.predict_probabilities(combined_features).iloc[-1]
    
    # -----------------------------------
    # 6. OUTPUT & DIAGNOSTICS
    # -----------------------------------
    print("\n" + "="*30)
    print(f"🚀 ENGINE STATUS: OPERATIONAL")
    print(f"📍 CURRENT STATE: {current_state}")
    print(f"📊 CONFIDENCE: {probs.max():.2%}")
    print("="*30)

    # Transition Matrix (How sticky is the current regime?)
    print("\nTransition Matrix (Stickiness):")
    print(hmm.get_transition_matrix().round(2))

    # PCA Loadings (What is driving the market right now?)
    print("\nTop PC1 Drivers (Market Force):")
    loadings = pca.get_loadings(forces.columns)
    print(loadings["PC1"].sort_values(ascending=False))

    # -----------------------------------
    # 7. REGIME CLASSIFICATION (The Final Label)
    # -----------------------------------
    scores = RegimeEngine.compute_scores(forces)
    regime, confidence = RegimeEngine.classify(scores)
    
    print(f"\nFinal Regime Logic Label: {regime.iloc[-1]}")
    print(f"Regime Logic Confidence: {confidence.iloc[-1]:.2f}")

if __name__ == "__main__":
    run_trading_engine()

