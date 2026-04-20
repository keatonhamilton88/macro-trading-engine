

class ExecutionMapper:
    # 1. The Strategy Gate: Which buckets are 'legal' in each regime?
    STRATEGY_GATE = {
        "deflation": ["duration_long", "vol_expansion", "liquidity_stress"],
        "risk_on":   ["growth_equity", "vol_compression", "fx_carry"],
        "inflation": ["commodity_long", "steepeners", "short_duration"],
        "risk_off":  ["vol_expansion", "short_equities", "long_dollar"]
    }

    # 2. Alpha Buckets: How the 6 forces (Growth, Inflation, Risk, etc.) impact the bucket
    ALPHA_BUCKETS = {
        "vol_compression": {"risk": -1.0, "credit": 0.5},
        "vol_expansion":   {"risk": 1.5, "credit": -0.5},
        "growth_equity":   {"growth": 1.0, "risk": -0.3},
        "liquidity_stress": {"dollar": 1.0, "credit": -0.8},
        "duration_long":   {"rates": -1.0, "growth": -0.5}
    }

    # 3. The "Toolbox" Product Map (Long and Short)
    PRODUCT_POOL = {
        "duration_long":    {"long": ["ZT=F", "ZN=F", "TLT"], "short": []},
        "vol_expansion":    {"long": ["VIX", "Long_Puts"], "short": ["SPY"]},
        "liquidity_stress": {"long": ["USDJPY=X", "DX-Y.NYB"], "short": ["EEM", "HYG"]},
        "commodity_long":   {"long": ["GC=F", "CL=F", "HG=F"], "short": []},
        "steepeners":       {"long": ["ZT=F"], "short": ["ZN=F"]} # Short the back, long the front
    }

    @staticmethod
    def get_strategy_proposal(regime_label, forces_today):
        """
        Generates a sophisticated proposal across the toolset.
        """
        allowed_strategies = ExecutionMapper.STRATEGY_GATE.get(regime_label, [])
        proposal = {}

        for strategy in allowed_strategies:
            # Check Fitness
            force_weights = ExecutionMapper.ALPHA_BUCKETS.get(strategy, {})
            fitness = sum(forces_today[f] * w for f, w in force_weights.items() if f in forces_today)
            
            if fitness > 0.5: # Threshold to ensure we don't trade 'noise'
                tools = ExecutionMapper.PRODUCT_POOL.get(strategy, {})
                proposal[strategy] = {
                    "confidence": round(fitness, 2),
                    "long": tools.get("long", []),
                    "short": tools.get("short", [])
                }
        
        return proposal
