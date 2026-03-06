import pandas as pd

class ForceVectorBuilder:

    @staticmethod
    def build_force(sensor_dict):
        df = pd.DataFrame(sensor_dict)
        return df.mean(axis=1)
    

