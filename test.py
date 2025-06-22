import osmnx as ox

# Define a region name
place_name = "Manawatu-Whanganui, New Zealand"

# Get the administrative boundary polygon
region = ox.geocode_to_gdf(place_name)

# Plot it or save it
region.plot()
region.to_file("manawatu_whanganui_boundary.geojson", driver="GeoJSON")
