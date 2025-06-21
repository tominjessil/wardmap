import geopandas as gpd
suburbs = gpd.read_file('nz-suburbs.geojson')
larger_area = gpd.read_file('detailed_suburbs.geojson')
suburbs = suburbs.to_crs("EPSG:2193")
larger_area = larger_area.to_crs("EPSG:2193")
clipped_suburbs = gpd.clip(suburbs, larger_area)
clipped_suburbs.to_crs("EPSG:4326").to_file("clipped-suburbs.geojson", driver="GeoJSON")
