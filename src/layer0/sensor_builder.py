from layer0.sensor_registry import SENSOR_REGISTRY

class SensorBuilder:

    def download_prices(self, tickers, start="2010-01-01"):

        data = yf.download(tickers, start=start)["Close"]

        if isinstance(data, pd.Series):
            data = data.to_frame()

        return data


    def build_sensors(self, prices):

        sensors = pd.DataFrame(index=prices.index)

        for name, fn in SENSOR_REGISTRY.items():

            sensors[name] = fn(prices)

        return sensors.dropna()


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



import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

    def analyze_sensor_correlations(builder_instance):
        """
        Calculates, visualizes, and identifies highly correlated sensors
        using a provided SensorBuilder instance.
    
        Args:
            builder_instance: An initialized instance of the SensorBuilder class.
        """
        print("Calculating sensor correlations...")
        corr = builder_instance.corr()
    
        print("Generating correlation heatmap...")
        plt.figure(figsize=(14,12))
        sns.heatmap(
            corr,
            cmap="coolwarm",
            center=0,
            annot=True, # Display the correlation values on the heatmap
            fmt=".2f"   # Format annotations to two decimal places
        )
        plt.title("Sensor Correlation Map")
        plt.show()
    
        print("\nIdentifying highly correlated sensors...")
        # Unstack the correlation matrix to get pairs, remove self-correlations
        corr_pairs = corr.unstack().sort_values(kind="quicksort")
        
        # Filter for high correlations (e.g., > 0.85) but less than perfect self-correlation (0.999 to avoid floating point issues)
        high_corr = corr_pairs[(corr_pairs > 0.85) & (corr_pairs < 0.999)]
    
        if not high_corr.empty:
            print("\nHighly Correlated Sensors (absolute correlation > 0.85):\n")
            print(high_corr)
        else:
            print("\nNo highly correlated sensors found (absolute correlation > 0.85).")
