# ==============================================
# LAYER 0 — Market Force Map
# ==============================================
class ForceLattice:
    def __init__(self, data: pd.DataFrame, lookback=252):
        self.data = data
        self.lookback = lookback
        self.z_scores = pd.DataFrame(index=data.index, columns=data.columns)
    
    def compute_z_scores(self):
        for col in self.data.columns:
            self.z_scores[col] = (
                (self.data[col] - self.data[col].rolling(self.lookback).mean()) /
                self.data[col].rolling(self.lookback).std()
            )
        return self.z_scores

    def aggregate_force_vectors(self, force_domains: dict):
        force_vectors = pd.DataFrame(index=self.data.index)
        for force_name, sensors in force_domains.items():
            force_vectors[force_name] = self.z_scores[sensors].mean(axis=1)
        return force_vectors

# ==============================================
# LAYER 1 — Product Architecture
# ==============================================
class ProductArchitecture:
    def __init__(self, engine_to_product: dict):
        """
        Map engines to tradable products
        """
        self.engine_to_product = engine_to_product
    
    def get_products(self, engine_name):
        return self.engine_to_product.get(engine_name, [])

# ==============================================
# LAYER 2 — Regime Matrix
# ==============================================
class RegimeMatrix:
    def __init__(self, regime_signatures: dict):
        self.regime_signatures = regime_signatures

# ==============================================
# LAYER 3 — Alpha Buckets
# ==============================================
class AlphaBuckets:
    def __init__(self, engines: dict):
        """
        engines: dict of {engine_name: {'weights': {force: w_i}}}
        """
        self.engines = engines
    
    def compute_fitness(self, regime_forces: pd.Series):
        fitness_scores = {}
        for engine, info in self.engines.items():
            weights = info['weights']
            fitness = sum(regime_forces[f] * w for f, w in weights.items() if f in regime_forces.index)
            fitness_scores[engine] = fitness
        return fitness_scores

# ==============================================
# LAYER 4 — Product Mapping
# ==============================================
class ProductMapping:
    def __init__(self, engine_to_products: dict):
        self.engine_to_products = engine_to_products
    
    def map_engine_to_products(self, engine_name):
        return self.engine_to_products.get(engine_name, [])

# ==============================================
# LAYER 5 — Indicator Computation
# ==============================================
class IndicatorFactory:
    def __init__(self, product_data: pd.DataFrame):
        self.product_data = product_data
    
    def compute_indicators(self):
        """
        Placeholder for all signal computations
        Example: moving averages, volatility, spreads, roll yield, skew, etc.
        """
        indicators = pd.DataFrame(index=self.product_data.index)
        # Example placeholder
        indicators['dummy_signal'] = self.product_data.mean(axis=1)
        return indicators

# ==============================================
# LAYER 6 — Market Regime Classification Engine
# ==============================================
class RegimeEngine:
    def __init__(self, force_vectors: pd.DataFrame, regime_signatures: dict,
                 confidence_threshold=0.35, persistence=3):
        self.force_vectors = force_vectors
        self.regime_signatures = regime_signatures
        self.confidence_threshold = confidence_threshold
        self.persistence = persistence
        self.active_regimes = pd.Series(index=force_vectors.index)
        self.confidence = pd.Series(index=force_vectors.index)
    
    def compute_similarity_scores(self):
        scores = pd.DataFrame(index=self.force_vectors.index)
        for regime, signature in self.regime_signatures.items():
            sig_vector = np.array([signature[f] for f in self.force_vectors.columns])
            scores[regime] = self.force_vectors.apply(lambda row: np.dot(row.values, sig_vector), axis=1)
        return scores
    
    def assign_regimes(self, scores: pd.DataFrame):
        for i in range(len(scores)):
            row = scores.iloc[i]
            best, second = row.nlargest(2)
            conf = (best - second) / abs(best) if best != 0 else 0
            self.confidence.iloc[i] = conf
            if conf > self.confidence_threshold:
                if i >= self.persistence:
                    recent = self.active_regimes.iloc[i-self.persistence:i]
                    if (recent == row.idxmax()).all():
                        self.active_regimes.iloc[i] = row.idxmax()
                    else:
                        self.active_regimes.iloc[i] = self.active_regimes.iloc[i-1]
                else:
                    self.active_regimes.iloc[i] = row.idxmax()
            else:
                self.active_regimes.iloc[i] = self.active_regimes.iloc[i-1] if i > 0 else row.idxmax()
        return self.active_regimes, self.confidence

# ==============================================
# LAYER 7 — Alpha Engine Factory
# ==============================================
class AlphaEngineFactory:
    def __init__(self, alpha_buckets: AlphaBuckets, strategy_gate: dict):
        self.alpha_buckets = alpha_buckets
        self.strategy_gate = strategy_gate  # {regime: allowed engines}
    
    def compute_alpha_weights(self, active_regime: str, regime_forces: pd.Series, sharpe_forecasts: dict):
        allowed_engines = self.strategy_gate.get(active_regime, [])
        fitness_scores = self.alpha_buckets.compute_fitness(regime_forces)
        weights = {}
        for engine in allowed_engines:
            weights[engine] = sharpe_forecasts.get(engine, 1.0) * fitness_scores.get(engine, 0.0)
        # normalize
        total = sum(abs(w) for w in weights.values()) or 1
        weights = {k: v/total for k, v in weights.items()}
        return weights

# ==============================================
# LAYER 8 — Risk Engine / Exposure Governor / Drawdown Firewall
# ==============================================
class RiskEngine:
    def __init__(self, macro_caps: dict, drawdown_limits: dict, correlation_matrix: pd.DataFrame):
        """
        macro_caps: {force: max_abs_exposure}
        drawdown_limits: {'daily': x%, 'cumulative': y%}
        correlation_matrix: instrument correlations for scaling
        """
        self.macro_caps = macro_caps
        self.drawdown_limits = drawdown_limits
        self.correlation_matrix = correlation_matrix
    
    def apply_risk_checks(self, proposed_weights: dict, portfolio_state: dict):
        """
        proposed_weights: {engine_name: weight}
        portfolio_state: current exposures, drawdowns
        Returns adjusted_weights
        """
        adjusted = proposed_weights.copy()
        # Macro exposure cap
        for engine, w in adjusted.items():
            # placeholder: scale down if exceeds macro caps
            pass
        # Correlation shrinkage
        # Drawdown check
        # Leverage / liquidity scaling
        # Final filtered weights
        return adjusted

# ==============================================
# End of 9-Layer Skeleton
# ==============================================
if __name__ == "__main__":
    print("Script is running")