import pandas as pd

from src.layer0.sensor_builder import SensorBuilder
from src.layer1.force_builder import ForceBuilder
from src.layer1.pca_engine import PCAEngine

# -----------------------------------
# 1. LOAD DATA
# -----------------------------------

builder = SensorBuilder()

tickers = [
    "HG=F","TIO=F","GC=F","CL=F","SI=F",
    "SOXX","SPY","ASHR","EEM","FXI",
    "AUDJPY=X","TLT","HYG",
    "^VIX","^VVIX","^VIX3M",
    "DX-Y.NYB","USDCNH=X","USDJPY=X","EURUSD=X","EURCHF=X",
    "ZN=F","SR3=F","ZT=F"
]

prices = builder.download_prices(tickers)

# -----------------------------------
# 2. BUILD SENSORS
# -----------------------------------

sensors = builder.build_sensors(prices)

print("\nSensors:")
print(sensors.tail())

# -----------------------------------
# 3. BUILD MACRO FORCES
# -----------------------------------

forces = ForceBuilder.build_forces(sensors)

print("\nForces:")
print(forces.tail())

# -----------------------------------
# 4. PCA OVERLAY
# -----------------------------------

# normalize sensors
z_sensors = (sensors - sensors.mean()) / sensors.std()

pca_engine = PCAEngine(n_components=3)
pc_df = pca_engine.fit_transform(z_sensors)

print("\nPCA Components:")
print(pc_df.tail())

# -----------------------------------
# 5. COMBINE FEATURES
# -----------------------------------

combined = pd.concat([forces, pc_df], axis=1)

print("\nCombined Feature Set:")
print(combined.tail())

from src.layer2.hmm_regime_engine import HMMRegimeEngine

# -----------------------------------
# HMM REGIME DETECTION
# -----------------------------------

hmm_engine = HMMRegimeEngine(n_states=4)

# fit model
hmm_engine.fit(combined)

# predict regimes
states = hmm_engine.predict_states(combined)

print("\nHMM States:")
print(states.tail())

# probabilities (confidence)
probs = hmm_engine.predict_probabilities(combined)

print("\nState Probabilities:")
print(probs.tail())

# transition matrix
print("\nTransition Matrix:")
print(hmm_engine.get_transition_matrix())

# -----------------------------------
# 6. PCA LOADINGS (INTERPRETATION)
# -----------------------------------

loadings = pca_engine.get_loadings(z_sensors.columns)

print("\nTop PC1 Drivers:")
print(loadings["PC1"].sort_values(ascending=False))




"""RegimeEngine"""

from src.layer2.regime_engine import RegimeEngine

# compute regime scores
scores = RegimeEngine.compute_scores(combined)

# classify regime
regime, confidence = RegimeEngine.classify(scores)

print("\nCurrent Regime:")
print(regime.tail())

print("\nConfidence:")
print(confidence.tail())
