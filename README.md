# Systematic Macro Trading Engine

Architecture:

Layer 0 — Market Force Map
Layer 1 — Regime Detection
Layer 2 — Strategy Selection
Layer 3 — Alpha Engines
Layer 4 — Portfolio Construction
Layer 5 — Risk Engine



macro-trading-engine/

README.md
.gitignore
requirements.txt

config/
    system_config.yaml
    data_sources.yaml

data/
    raw/
    processed/
    cache/

src/
    data/
        data_loader.py
        api_clients.py

    features/
        zscore.py
        rolling_stats.py
        transforms.py

    layer0/
        sensors.py
        force_vectors.py
        force_table.py

    regime/
        regime_classifier.py
        regime_matrix.py

    alpha/
        trend_engine.py
        carry_engine.py
        mean_reversion_engine.py

    portfolio/
        capital_router.py
        exposure_engine.py

    risk/
        drawdown_firewall.py
        exposure_caps.py

research/
    notebooks/

tests/
    test_zscore.py
    test_force_vectors.py
