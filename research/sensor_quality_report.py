import pandas as pd 
# Sensor Quality Control Add-on
    def check_sensor_quality(sensors):

            report = {}

    for col in sensors.columns:

        series = sensors[col]

        report[col] = {
            "missing_pct": series.isna().mean(),
            "std": series.std(),
            "latest": series.iloc[-1]
        }

    return pd.DataFrame(report)
