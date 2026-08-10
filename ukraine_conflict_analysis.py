import geopandas as gpd
oblasts = gpd.read_file('data/boundaries/geoBoundaries-UKR-ADM1-all/geoBoundaries-UKR-ADM1.geojson')
print(oblasts.head())
