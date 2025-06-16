import geopandas as gpd

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
