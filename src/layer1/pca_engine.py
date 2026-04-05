from sklearn.decomposition import PCA
import pandas as pd


class PCAEngine:

    # The three components are PC1 - master force(beta/trend), PC2 - volatility/stress capturing risk/growth, PC3 - rotation between forces
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

    # important "diagnostic" tool. It tells you exactly which sensors are in the driver's seat.
    def get_loadings(self, sensor_columns):

        return pd.DataFrame(
            self.model.components_.T,
            index=sensor_columns,
            columns=[f"PC{i+1}" for i in range(self.n_components)]
        )


    
    def get_explained_variance(self):
    """
    Returns the % of market movement explained by each PC.
    If PC1 + PC2 < 50%, the market is too noisy to trade.
    """
        return pd.Series(
            self.model.explained_variance_ratio_,
            index=[f"PC{i+1}" for i in range(self.n_components)],
            name="Explained Variance"
        )
