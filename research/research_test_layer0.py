from data_loader import YFinanceLoader
from layer0_sensors import SensorLibrary

loader = YFinanceLoader()

spy = loader.load_close("SPY")
tlt = loader.load_close("TLT")  
gld = loader.load_close("GLD")

risk = SensorLibrary.equity_risk_appetite(spy)
bond = SensorLibrary.bond_momentum(tlt)
gold = SensorLibrary.gold_safety(gld)

print(risk.tail())
print(bond.tail())
print(gold.tail())
