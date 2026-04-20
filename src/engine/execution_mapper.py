# src/engine/execution_mapper.py

class ExecutionMapper:
    # THE COMPLETE TOOLBOX
    TOOLBOX = {
        "micro_indices": ["MES", "MNQ"],
        "energy":        ["CL", "MNG"],
        "metals":        ["GC", "HG", "SI"],
        "ags":           ["ZS", "ZW", "ZC", "KE"],
        "crypto_micro":  ["MBT", "MET"],
        "fx_futures":    ["6A", "6B", "6C", "6E", "6J", "6M", "6N", "6S", "DX"],
        "fx_cash":       ["AUD.CAD", "CAD.USD", "AUD.JPY", "AUD.USD", "EUR.USD"],
        "rates":         ["ZT", "ZN", "SR3"],
        "options":       ["SPY_PUT", "SPY_STRANGLE", "VIX_CALL"]
    }

    # THE STRATEGY MAP (The 'Where')
    STRATEGY_GATE = {
        "deflation": ["duration_long", "liquidity_stress"],
        "risk_on":   ["growth_equity", "vol_compression", "fx_carry"],
        "inflation": ["commodity_long", "steepeners"],
        "risk_off":  ["vol_expansion", "short_equities", "duration_long"]
    }

    # MAPPING BUCKETS TO TOOLBOX CATEGORIES
    BUCKET_ASSETS = {
        "duration_long":    ["rates"],
        "liquidity_stress": ["fx_futures", "fx_cash"],
        "growth_equity":    ["micro_indices", "crypto_micro"],
        "vol_compression":  ["options"], # Specifically Strangles
        "vol_expansion":    ["options", "fx_futures"], # Puts and DX
        "commodity_long":   ["energy", "metals", "ags"],
        "steepeners":       ["rates"] # Spread logic
    }

    @staticmethod
    def rank_tactical_entries(bucket_name, prices_df):
        """
        Merged Tactical Ranker:
        1. Gets all potential tools for a bucket.
        2. Scans RSI/EMA/ATR (Layer 5) to pick the 'best' entry.
        """
        categories = ExecutionMapper.BUCKET_ASSETS.get(bucket_name, [])
        candidates = []
        for cat in categories:
            candidates.extend(ExecutionMapper.TOOLBOX.get(cat, []))
            
        # TACTICAL FILTER (Pseudo-code for Layer 5 integration)
        # 1. Filter for Price > EMA 200 (Trend)
        # 2. Rank by RSI (Strength)
        # 3. Size by ATR (Risk)
        
        # For now, return the full candidate list sorted
        return candidates

    @staticmethod
    def get_trade_proposal(regime_label, forces_today, prices_df):
        allowed_strats = ExecutionMapper.STRATEGY_GATE.get(regime_label, [])
        proposal = {}

        for strat in allowed_strats:
            # (Fitness logic remains here)
            # ...
            
            # The Tactical Scan happens here
            best_tools = ExecutionMapper.rank_tactical_entries(strat, prices_df)
            proposal[strat] = {"best_tools": best_tools}
            
        return proposal

