import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point
from shapely.ops import split

# Load GeoJSON (in EPSG:4326)
gdf = gpd.read_file('nz-suburbs-v2.geojson')

# Reproject to NZTM2000 (EPSG:2193) for splitting
gdf = gdf.to_crs("EPSG:2193")

# Select the suburb to split
target_suburb_name = 'Tararua Forest Park'
target_suburb = gdf[gdf['name'] == target_suburb_name].iloc[0]
geom = target_suburb.geometry

# Define the two points (still in EPSG:4326)
point1 = Point(175.36144199566823, -40.72643899978211)
point2 = Point(175.58627599213145, -40.73565500053768)

# Create GeoSeries to reproject both points
points = gpd.GeoSeries([point1, point2], crs="EPSG:4326").to_crs("EPSG:2193")

# Build cutting line using projected coordinates
cutting_line = LineString([
    (points[0].x, points[0].y),
    (points[1].x, points[1].y)
])

# Perform the split
split_result = split(geom, cutting_line)

# Create new rows for each resulting polygon
new_rows = []
for i, part in enumerate(split_result.geoms):
    new_row = target_suburb.copy()
    new_row['geometry'] = part
    new_row['name'] = f"{target_suburb_name}_part_{i+1}"
    new_rows.append(new_row)

# Create new GeoDataFrame from the split parts
split_gdf = gpd.GeoDataFrame(new_rows, columns=gdf.columns, crs=gdf.crs)

# Replace original suburb with split ones
gdf = gdf[gdf['name'] != target_suburb_name]
gdf = pd.concat([gdf, split_gdf], ignore_index=True)

# Reproject back to EPSG:4326 for saving
gdf = gdf.to_crs("EPSG:4326")

# Save updated GeoJSON
gdf.to_file('suburbs_split.geojson', driver='GeoJSON')

print("Suburb successfully split with your custom line!")
