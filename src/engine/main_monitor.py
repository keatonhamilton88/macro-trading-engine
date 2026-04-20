import time
import numpy as np
import pandas as pd
from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine
from src.layer2.hmm_regime_engine import HMMRegimeEngine
from src.engine.exit_engine import DynamicExitEngine
from src.engine.order_submitter import OrderSubmitter

def run_daily_monitor():
    # 1. RUN THE BRAIN (The Stack)
    forces, pc_df, hmm, combined = run_macro_stack(ib, sb, fb)
    current_regime = hmm.predict_states(combined).iloc[-1]
    latest_forces = forces.iloc[-1]
    
    # 2. EVALUATE EXITS (Defense First)
    open_positions = ib.positions()
    for pos in open_positions:
        ticker = pos.contract.symbol
        # Layer 5: Calculate RSI/EMA/Vol on the fly
        indicators = compute_tactical_indicators(ticker)
        
        action, reason = DynamicExitEngine.evaluate_exits(
            ticker, pos, current_regime, indicators, pc_df.iloc[-1]
        )
        
        if action == "EXIT_NOW":
            # Immediate Market Exit for Macro Regime flips
            print(f"🔥 MACRO KILL: Closing {ticker} | Reason: {reason}")
            order_submitter.close_position(pos)
            
        elif action == "TAKE_PROFIT":
            # Scale out 50% for Tactical Exhaustion (RSI/Vol signal)
            print(f"💰 HARVESTING: Scaling 50% of {ticker} | Reason: {reason}")
            order_submitter.scale_out(pos, 0.5)

    # 3. SCAN FOR NEW OPPORTUNITIES (Offense Second)
    # Freed-up margin from Step 2 is now available in your 'Excess Liquidity'
    account = ib.accountSummary()
    excess_liq = float([tag.value for tag in account if tag.tag == 'ExcessLiquidity'][0])

    # Only look for new trades if we have our 30% margin buffer intact
    if excess_liq > (total_equity * 0.30):
        print("🔍 Scanning for new entries with available Dry Powder...")
        proposal = execution_mapper.get_trade_proposal(current_regime, latest_forces)
        # Final gate: Risk Engine validates and sizes
        process_new_trades(proposal, excess_liq)
