from src.layer0.sensor_builder import SensorBuilder
from src.layer0.force_table import ForceTableBuilder


builder = SensorBuilder()

tickers = [
    "HG=F",     # copper
    "GC=F",     # gold
    "CL=F",     # oil
    "SPY",
    "TLT",
    "HYG",
    "LQD",
    "EEM",
    "AUDJPY=X",
    "^VIX"
]

prices = builder.download_prices(tickers)

sensors = builder.build_sensors(prices)

print("\nSensors")
print(sensors.tail())


force_table = ForceTableBuilder.build(sensors)

print("\nForce Table")
print(force_table.tail())
