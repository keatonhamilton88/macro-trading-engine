import pandas as pd
from src.features.transforms import z_score


class ForceBuilder:

    @staticmethod
    def build_forces(sensor_df, lookback=252):

        forces = pd.DataFrame(index=sensor_df.index)

        for col in sensor_df.columns:
            force_name = col.replace("_sensor", "_force")
            forces[force_name] = z_score(sensor_df[col], lookback)

        return forces
