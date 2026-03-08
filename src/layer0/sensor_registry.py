from layer0.sensors.growth import growth_sensor
from layer0.sensors.inflation import inflation_sensor
from layer0.sensors.risk import risk_sensor
from layer0.sensors.credit import credit_sensor
from layer0.sensors.em import em_sensor
from layer0.sensors.carry import carry_sensor
from layer0.sensors.dollar import dollar_sensor
from layer0.sensors.volatility import vol_sensor


SENSOR_REGISTRY = {

    "growth_sensor": growth_sensor,
    "inflation_sensor": inflation_sensor,
    "risk_sensor": risk_sensor,
    "credit_sensor": credit_sensor,
    "em_sensor": em_sensor,
    "carry_sensor": carry_sensor,
    "dollar_sensor": dollar_sensor,
    "vol_sensor": vol_sensor

}
