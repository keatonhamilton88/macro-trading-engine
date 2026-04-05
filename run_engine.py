# 1. Build your 6 Market Forces
forces_df = ForceBuilder.build_forces(sensor_df)

# 2. Initialize the Engine
pca_engine = PCAEngine(n_components=3)

# 3. Transform the Forces into PC Signals
# .dropna() is critical because PCA cannot handle NaNs from your lookback
pc_signals = pca_engine.fit_transform(forces_df.dropna())

# 4. Check which Force is dominating PC1
loadings = pca_engine.get_loadings(forces_df.columns)
print(loadings['PC1'].sort_values(ascending=False))

