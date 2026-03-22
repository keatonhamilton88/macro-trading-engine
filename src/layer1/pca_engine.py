from sklearn.decomposition import PCA
import pandas as pd


class PCAEngine:

    def __init__(self, n_components=3):
        self.n_components = n_components
        self.model = PCA(n_components=n_components)

    def fit_transform(self, z_sensors):

        pc_values = self.model.fit_transform(z_sensors)

        pc_df = pd.DataFrame(
            pc_values,
            index=z_sensors.index,
            columns=[f"PC{i+1}" for i in range(self.n_components)]
        )

        return pc_df

    def get_loadings(self, sensor_columns):

        return pd.DataFrame(
            self.model.components_.T,
            index=sensor_columns,
            columns=[f"PC{i+1}" for i in range(self.n_components)]
        )
