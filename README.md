# Systematic Macro Trading Engine

Architecture:

Layer 0 — Market Force Map
Layer 1 — Regime Detection
Layer 2 — Strategy Selection
Layer 3 — Alpha Engines
Layer 4 — Portfolio Construction
Layer 5 — Risk Engine



macro-trading-engine/

__pycache__
    data_loader.cpython-314.pyc
    features.cpython-314.pyc
    layer0_force_vectors.cpython-314.pyc
    layer0_sensors.cpython-314.pyc

data
    processed
    raw

research
    __init__.py
    run_sensor_analysis.py
    sensor_correlation_map.py
    sensor_diagnostics.py
    sensor_quality_report.py
    test_layer0.py
    test_sensors.py

src
    data
    __init__.py
    data_loader.py
    engine
    __init__.py
    algo_trader.py
    layer-build.py
features
     __init__.py
    feature_engineering.py
    normalization.py
    rolling_stats.py
    transforms.py
    volatility.py
layer0
    sensors
        __init__.py
        ashr_spy.py
        aud_jpy.py
        cl_gc.py
        dx.py
        eem_spy.py
        eur_chf.py
        eur_usd.py
        fxi.py
        gamma_flip.py
        gc_si.py
        hg_cl.py
        hg_gc.py
        hg_tio.py
        hyg_tlt.py
        put_call_ratio.py
        sox_spy.py
        spx_gex.py
        spy_tlt.py
        usd_cnh.py
        usd_jpy.py
        vix.py
        vix_slope.py
        vix_vol.py
        zero_dte_vol.py
        zn_sr3.py
        zn_zt.py
        __init__.py
    force_builder.py
    force_table.py   
    force_vectors.py
    sensor_builder.py
    sensor_registry.py

regime
    __init__.py
    macro-momentum-regime-model.py

tests
    test.py
    test_data.py
    test_zscore.py
    __init__.py

.gitignore

README.md

requirements.txt

run_engine.py
