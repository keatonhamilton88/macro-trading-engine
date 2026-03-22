from src.layer1.pca_engine import PCAEngine
from src.features.transforms import z_score

# normalize sensors
z_sensors = sensors.apply(lambda x: z_score(x))

# run PCA
pca_engine = PCAEngine(n_components=3)
pc_df = pca_engine.fit_transform(z_sensors)

print(pc_df.tail())


combined = pd.concat([forces, pc_df], axis=1)


loadings = pca_engine.get_loadings(z_sensors.columns)

print(loadings["PC1"].sort_values(ascending=False))
