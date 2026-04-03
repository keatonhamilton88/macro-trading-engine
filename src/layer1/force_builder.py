import pandas as pd
from transforms import zscore_returns


class ForceBuilder:

    FORCE_MAP = {

        "growth": [
            "hg_gc",
            "sox_spy",
            "ashr_spy",
            "eem_spy",
            "aud_jpy"
        ],

        "inflation": [
            "cl_gc",
            "hg_cl",
            "gc_si",
            "hg_tio"
        ],

        "risk": [
            "vix",
            "vix_vol",
            "vix_slope",
            "gamma_flip",
            "spx_gex"
        ],

        "dollar": [
            "dx",
            "usd_cnh",
            "eur_usd",
            "usd_jpy",
            "eur_chf"
        ],

        "credit": [
            "hyg_tlt",
            "spy_tlt"
        ],

        "rates": [
            "zn_sr3",
            "zn_zt"
        ]
    }

    @staticmethod
    def build_forces(sensor_df, lookback=252):

        # normalize sensors first
        z_sensors = sensor_df.apply(lambda x: z_score(x, lookback))

        forces = pd.DataFrame(index=sensor_df.index)

        for force_name, sensor_list in ForceBuilder.FORCE_MAP.items():

            valid_sensors = [s for s in sensor_list if s in z_sensors.columns]

            if len(valid_sensors) > 0:
                forces[force_name] = z_sensors[valid_sensors].mean(axis=1)

        return forces
