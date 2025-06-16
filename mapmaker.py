import geopandas as gpd
import folium
from folium import Element

# Load your GeoJSON
# gdf = gpd.read_file("lds-nz-suburbs-and-localities-SHP/nz-suburbs-and-localities.shp")
# gdf = gdf.to_crs(epsg=4326)

# # Save as GeoJSON
# gdf.to_file("nz-suburbs.geojson", driver="GeoJSON")

gdf = gpd.read_file("nz-suburbs.geojson")

# Your ward assignments
ward_groups = {
    "Holy Family": ["Avalon", "Belmont", "Boulcott", "Epuni", "Harbour View", "Kelson", "Tirohanga"],
    "St. Thomas": ["Petone", "Eastbourne", "Naenae", "Korokoro", "Waiwhetū", "Woburn", "Waterloo",
                   "Hutt Central", "Wainuiomata", "Seaview", "Alicetown"],
    "St. Francis Xavier": ["Stokes Valley", "Taitā", "Manor Park"],
    "St. Joseph’s": ["Silverstream", "Pinehaven", "Blue Mountains", "Heretaunga", "Trentham",
                     "Riverstone Terraces", "Haywards", "Wallaceville", "Elderslea", "Ebdentown",
                     "Whitemans Valley", "Kingsley Heights", "Clouston Park", "Tōtara Park",
                     "Maoribank", "Brown Owl", "Mangaroa", "Timberlea", "Birchville", "Te Mārua",
                     "Kaitoke", "Akatarawa"],
    "Kapiti": ["Raumati Beach", "Raumati South", "Maungakōtukutuku", "Paraparaumu",
               "Paraparaumu Beach", "Otaihanga", "Waikanae", "Waikanae Beach",
               "Peka Peka", "Reikorangi"],
    "St. Chavara": ["Miramar", "Kilbirnie", "Island Bay", "Berhampore", "Newtown", "Brooklyn",
                    "Aro Valley", "Mount Cook", "Kelburn", "Thorndon", "Wadestown", "Hataitai"],
    "St Alphonsa": ["Tawa", "Churton Park", "Glenside", "Grenada North", "Grenada Village",
                    "Horokiwi", "Johnsonville", "Newlands", "Ohariu", "Paparangi", "Takapu Valley",
                    "Woodridge", "Broadmeadows", "Crofton Downs", "Kaiwharawhara", "Karori",
                    "Khandallah", "Mākara", "Mākara Beach", "Ngaio", "Ngauranga", "Northland",
                    "Wadestown", "Wilton", "Aotea", "Ascot Park", "Cannons Creek", "Elsdon",
                    "Kenepuru", "Mana Island", "Porirua City Centre", "Rānui", "Takapūwāhia",
                    "Tītahi Bay", "Waitangirua", "Camborne", "Hongoeka", "Judgeford", "Pukerua Bay",
                    "Paekākāriki Hill", "Papakōwhai", "Paremata", "Pāuatahanui", "Plimmerton", "Whitby"]
}

# Color for each ward
group_colors = {
    "Holy Family": "#e6194b",     # red
    "St. Thomas": "#4363d8",      # green
    "St. Francis Xavier": "#73cd85",  # yellow
    "St. Joseph’s": "#f58231",    # blue
    "Kapiti": "#cec93e",          # orange
    "St. Chavara": "#911eb4",     # purple
    "St Alphonsa": "#b27b53"      # cyan
}

# Helper: find ward
def get_ward(suburb):
    for ward, suburbs in ward_groups.items():
        if suburb in suburbs:
            return ward
    return None

# Apply color to each row
def get_fill_color(suburb):
    ward = get_ward(suburb)
    return group_colors.get(ward, "rgba(0,0,0,0)")  # grey fallback

# Add or update 'fill' and 'ward'
gdf["ward"] = gdf["name"].apply(get_ward)
gdf["fill"] = gdf["name"].apply(get_fill_color)
gdf["fill-opacity"] = 0.6
gdf["stroke"] = "#555555"
gdf["stroke-width"] = 1
gdf["stroke-opacity"] = 1

# Export to GeoJSON
gdf.to_file("suburbs_colored.geojson", driver="GeoJSON")

# Create base map centered on NZ (or adjust to your data)
m = folium.Map(location=[-41.2, 174.8], zoom_start=15, tiles="CartoDB Positron", max_bounds=True)

# Add your colored GeoJSON to the map
folium.GeoJson(
    "suburbs_colored.geojson",
    name="Wards",
    style_function=lambda feature: {
        'fillColor': feature['properties'].get('fill', 'gray'),
        'color': feature['properties'].get('stroke', '#000000'),
        'weight': feature['properties'].get('stroke-width', 1),
        'fillOpacity': feature['properties'].get('fill-opacity', 0.6),
        'opacity': feature['properties'].get('stroke-opacity', 1),
    },
    tooltip=folium.GeoJsonTooltip(fields=["name", "ward"], aliases=["Suburb", "Ward"])
).add_to(m)

m.fit_bounds([[-41.5, 174.5], [-39.5, 176.5]])

# Legend HTML
legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 160px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding: 10px;
    box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    ">
    <b>Ward Legend</b><br>
    <i style="background:#e6194b; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> Holy Family<br>
    <i style="background:#4363d8; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St. Thomas<br>
    <i style="background:#73cd85; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St. Francis Xavier<br>
    <i style="background:#f58231; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St. Joseph’s<br>
    <i style="background:#cec93e; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> Kapiti<br>
    <i style="background:#911eb4; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St. Chavara<br>
    <i style="background:#b27b53; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St Alphonsa<br>
</div>
"""

legend = Element(legend_html)
m.get_root().html.add_child(legend)

# Save the map
m.save("index.html")