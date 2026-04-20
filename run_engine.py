import pandas as pd
import numpy as np
from ib_insync import util

# Core Layer Imports
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.layer2.hmm_regime_engine import HMMRegimeEngine
from src.layer2.regime_engine import RegimeEngine

# Data and Engine Imports
from src.data.ibkr_connector import IBKRConnector
from src.data.data_loader import get_last_valid_trading_date
from src.engine.execution_mapper import ExecutionMapper

def run_trading_engine():
    # -----------------------------------
    # 1. INITIALIZE IBKR CONNECTION
    # -----------------------------------
    # Ensure TWS or IB Gateway is running on port 7497
    connector = IBKRConnector(host='127.0.0.1', port=7497, client_id=1)
    try:
        connector.connect()
    except Exception as e:
        print(f"❌ Connection Failed: {e}. Is TWS/Gateway running?")
        return

    # -----------------------------------
    # 2. DATA INGESTION (Layers 0-1)
    # -----------------------------------
    # The connector handles the Toolbox tickers and 2-year lookback
    builder = SensorBuilder(ib_connector=connector)
    
    print("--- 📥 Downloading IBKR Institutional Data ---")
    prices = builder.download_prices() 
    
    # Add the mock Gamma Flip column (until you integrate a live GEX feed)
    prices['SPX_GEX_FLIP'] = 5000.0 

    # 3. Build Sensors (Layer 0)
    print("--- 🛠 Building Sensors (Layer 0) ---")
    sensors = builder.build_sensors(prices)
    # Patch any gaps for the math models
    sensors = sensors.ffill().fillna(0)

    # -----------------------------------
    # 3. BUILD MACRO FORCES (Layer 1)
    # -----------------------------------
    print("--- 🌊 Aggregating Market Forces (Layer 1) ---")
    forces = ForceBuilder.build_forces(sensors)
    
    # 1. Determine the valid trading date
    valid_date = get_last_valid_trading_date(forces)
    
    if not valid_date:
        print("❌ Error: No valid trading data found.")
        connector.ib.disconnect()
        return

    # 2. Slice forces to the valid date and check history
    forces = forces.loc[:valid_date]
    print(f"📅 Last Valid Trading Day: {valid_date.date()}")

    if len(forces) < 252:
        print(f"❌ Error: Insufficient history ({len(forces)} days). Need 252 for warm-up.")
        connector.ib.disconnect()
        return

    # -----------------------------------
    # 4. PCA ENGINE (Layer 1.5)
    # -----------------------------------
    print("--- 🔬 Running PCA Engine ---")
    pca = PCAEngine(n_components=3)
    pc_df = pca.fit_transform(forces) 
    
    # -----------------------------------
    # 5. HMM REGIME DETECTION (Layer 2)
    # -----------------------------------
    print("--- 🧠 Detecting Market Regimes (Layer 2) ---")
    combined_features = pd.concat([forces, pc_df], axis=1).dropna()
    
    hmm = HMMRegimeEngine(n_states=4)
    hmm.fit(combined_features)
    
    # Extract current state and probabilities
    current_state = hmm.predict_states(combined_features).loc[valid_date]
    probs = hmm.predict_probabilities(combined_features).loc[valid_date]
    
    # -----------------------------------
    # 6. OUTPUT & DIAGNOSTICS
    # -----------------------------------
    print("\n" + "="*30)
    print(f"🚀 ENGINE STATUS: OPERATIONAL")
    print(f"📍 HMM STATE: {current_state}")
    print(f"📊 CONFIDENCE: {probs.max():.2%}")
    print("="*30)

    p_today = pc_df.loc[valid_date]
    print(f"\n✅ PCA Success | PC1 (Beta): {p_today['PC1']:.2f}")
    
    # -----------------------------------
    # 7. REGIME CLASSIFICATION (The Logic Label)
    # -----------------------------------
    scores = RegimeEngine.compute_scores(forces)
    regime_label, confidence = RegimeEngine.classify(scores)
    current_regime = regime_label.loc[valid_date]
    
    print(f"\nFinal Logic Label: {current_regime}")
    print(f"Logic Confidence: {confidence.loc[valid_date]:.2f}")

    # -----------------------------------
    # 8. EXECUTION PROPOSAL (Layer 3-7)
    # -----------------------------------
    print("\n" + "🎯 STRATEGY PROPOSAL " + "="*10)
    
    # Use valid date forces for the proposal
    f_today = forces.loc[valid_date]
    trade_proposal = ExecutionMapper.get_trade_proposal(current_regime, f_today, prices)

    if not trade_proposal:
        print("Neutral - No strategy meets fitness threshold.")
    else:
        for strat, details in trade_proposal.items():
            print(f"▶ {strat.upper()} (Fit: {details.get('fit', 'N/A')})")
            # Using our merged 'best_tools' logic
            print(f"   Recommended Tools: {details.get('best_tools', [])}")

    print("\n--- 🏁 ENGINE RUN COMPLETE ---")
    
    # Disconnect when done
    connector.ib.disconnect()

if __name__ == "__main__":
    run_trading_engine()

