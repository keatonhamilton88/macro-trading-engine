import sys
sys.path.append("src")

from layer0.sensor_builder import SensorBuilder
from sensor_correlation_map import analyze_sensor_correlations


builder = SensorBuilder()

tickers = [
    "HG=F","GC=F","CL=F","SPY","TLT","HYG",
    "FXI","SOXX","AUDJPY=X","DX-Y.NYB","^VIX"
]

prices = builder.download_prices(tickers)

sensors = builder.build_sensors(prices)

analyze_sensor_correlations(sensors)
