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

print("\nSensors")
print(sensors.tail())

forces = ForceBuilder.build_forces(sensors)

print("\nForces")
print(forces.tail())
