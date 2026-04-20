class DynamicExitEngine:
    @staticmethod
    def evaluate_exits(ticker, position, current_regime, indicators, pca_signals):
        """
        Re-evaluates every bar: Does the macro still support this trade?
        """
        # 1. REGIME CHECK (The HMM 'Kill Switch')
        # If we are LONG but the regime is now DEFLATION or RISK_OFF
        if position.amount > 0 and current_regime in ["deflation", "risk_off"]:
            return "EXIT_NOW", "Macro Regime Invalidation"

        # 2. RSI EXHAUSTION (The Tactical Exit)
        # Long position + RSI overbought + Volume dropping
        if position.amount > 0 and indicators['rsi'] > 75:
            if indicators['vol_change'] < 0: # Volume drying up
                return "TAKE_PROFIT", "Tactical Exhaustion"

        # 3. MOMENTUM SLOWDOWN (The Trailing Stop)
        # Price crossing below a fast EMA (e.g., 20)
        if position.amount > 0 and indicators['price'] < indicators['ema_20']:
            return "EXIT_TRAILING", "Trend Decay"

        # 4. PCA REVERSAL
        # If PC1 (Market Force) flips direction sharply
        if abs(pca_signals['pc1_change']) > 1.5: # 1.5 SD move against us
            return "EXIT_NOW", "PCA Force Reversal"

        return "HOLD", "Signal Intact"
