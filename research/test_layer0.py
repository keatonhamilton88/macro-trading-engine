from src.layer0.sensor_builder import SensorBuilder
from src.layer0.force_builder import ForceBuilder

builder = SensorBuilder()

prices = builder.download_prices([
    "HG=F",
    "GC=F",
    "CL=F",
    "SPY",
    "^VIX"
])

sensors = builder.build_sensors(prices)

print("\nSensors")
print(sensors.tail())

forces = ForceBuilder.build_forces(sensors)

print("\nForces")
print(forces.tail())
