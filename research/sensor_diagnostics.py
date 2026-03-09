from src.layer0.sensor_builder import SensorBuilder
import seaborn as sns
import matplotlib.pyplot as plt
from features import z_score

z_sensors = sensors.applya(z_score)


builder = SensorBuilder()

prices = builder.download_prices(tickers)

sensors = builder.build_sensors(prices)

corr = sensors.corr()

sns.heatmap(corr, cmap="coolwarm", center=0)

plt.show()
