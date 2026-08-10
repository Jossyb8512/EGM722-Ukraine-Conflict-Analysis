import geopandas as gpd
import matplotlib.pyplot as plt
oblasts = gpd.read_file('data/boundaries/geoBoundaries-UKR-ADM1-all/geoBoundaries-UKR-ADM1.geojson')
print(oblasts.head())
print(oblasts.columns)
print(oblasts.crs)
print(f"Number of administrative regions: {len(oblasts)}")
print(oblasts['shapeName'].tolist())
oblasts.plot()
plt.show()