from src.layer0.sensor_builder import SensorBuilder


builder = SensorBuilder()

tickers = [
    "HG=F",   # copper
    "GC=F",   # gold
    "CL=F",   # oil
    "SPY",
    "TLT",
    "HYG",
    "LQD",
    "EEM",
    "AUDJPY=X",
    "DX-Y.NYB",
    "^VIX"
]

prices = builder.download_prices(tickers)

sensors = builder.build_sensors(prices)

print(sensors.tail())
