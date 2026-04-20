import time
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.layer2.hmm_regime_engine import HMMRegimeEngine
from src.engine.exit_engine import DynamicExitEngine
from src.engine.order_submitter import OrderSubmitter

def run_daily_monitor():
    # 1. FETCH & PROCESS (Layers 0-1.5)
    # Get prices, build sensors, aggregate forces, run PCA
    prices, sensors, forces, pc_df = run_macro_stack() 
    
    # 2. IDENTIFY REGIME (Layer 2)
    # HMM determines if we are in 'Risk-On', 'Deflation', etc.
    current_regime = hmm.predict_states(combined_features).iloc[-1]

    # 3. MONITOR OPEN POSITIONS (The Dynamic Exit)
    open_positions = ib.positions()
    for pos in open_positions:
        ticker = pos.contract.symbol
        # Get latest RSI, EMA, Volume for this specific ticker
        indicators = compute_tactical_indicators(ticker) 
        
        # ASK THE EXIT ENGINE: "Kill or Keep?"
        action, reason = DynamicExitEngine.evaluate_exits(
            ticker, pos, current_regime, indicators, pc_df.iloc[-1]
        )
        
        if action != "HOLD":
            print(f"🚨 EXIT SIGNAL: {ticker} | Reason: {reason}")
            order_submitter.close_position(pos)

    # 4. SCAN FOR NEW ENTRIES (The Strategy Gate)
    # If we have spare margin, check if the Regime allows new trades
    if has_excess_margin():
        check_for_new_opportunities(current_regime, forces.iloc[-1])

if __name__ == "__main__":
    while True:
        # In production, this would sleep until the market is near-close
        run_daily_monitor()
        time.sleep(86400) # Wait 24 hours
