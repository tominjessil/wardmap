import geopandas as gpd
import folium
from branca.element import Template, MacroElement

# Load your data
gdf = gpd.read_file("lds-nz-suburbs-and-localities-SHP/nz-suburbs-and-localities.shp")

# Convert CRS to WGS84 (lat/lon) for Folium
gdf = gdf.to_crs(epsg=4326)

# Create a base map centered on Wellington
m = folium.Map(location=[-41.2865, 174.7762], zoom_start=12, tiles="Mapbox Bright", attr="Map data ©")



# -------------------------------------------
# Define suburb groups and associated colors
# -------------------------------------------
# Example: Assume the 'NAME' column contains suburb names
ward_groups = {
    "Holy Family": [
        "Avalon", "Belmont", "Boulcott", "Epuni", "Harbour View", "Kelson", "Tirohanga"
    ],
    "St. Thomas": [
        "Petone", "Eastbourne", "Naenae", "Korokoro", "Waiwhetū", "Woburn", "Waterloo",
        "Hutt Central", "Wainuiomata", "Seaview", "Alicetown"
    ],
    "St. Francis Xavier": [
        "Stokes Valley", "Taitā", "Manor Park"
    ],
    "St. Joseph’s": [
        "Silverstream", "Pinehaven", "Blue Mountains", "Heretaunga", "Trentham",
        "Riverstone Terraces", "Haywards", "Wallaceville", "Elderslea", "Ebdentown",
        "Whitemans Valley", "Kingsley Heights", "Clouston Park", "Tōtara Park",
        "Maoribank", "Brown Owl", "Mangaroa", "Timberlea", "Birchville", "Te Mārua",
        "Kaitoke", "Akatarawa"
    ],
    "Kapiti": [
        "Raumati Beach", "Raumati South", "Maungakōtukutuku", "Paraparaumu",
        "Paraparaumu Beach", "Otaihanga", "Waikanae", "Waikanae Beach",
        "Peka Peka", "Reikorangi"
    ],
    "St. Chavara": [
        "Miramar", "Kilbirnie", "Island Bay", "Berhampore", "Newtown", "Brooklyn",
        "Aro Valley", "Mount Cook", "Kelburn", "Thorndon", "Wadestown", "Hataitai"
    ],
    "Ocean":[
        "Cook Strait", "Palliser Bay", "Wellington Harbour / Port Nicholson", "Browns Bay", "Bradeys Bay", "Te Awarua-o-Porirua Harbour (Pauatahanui Arm)", 
        "Onehunga Bay", "Te Awarua-o-Porirua Harbour", "Karehana Bay", "Hongoeka Bay", "Ivey Bay", "Open Bay", "Tirau Bay", "Wharehou Bay", "Ohariu Bay", "Lake Wairarapa"
    ],
    "St Alphonsa": [
        "Tawa", "Churton Park", "Glenside", "Grenada North", "Grenada Village", "Horokiwi", "Johnsonville", "Newlands", 
        "Ohariu", "Paparangi", "Takapu Valley", "Woodridge", "Broadmeadows", "Crofton Downs", "Kaiwharawhara", "Karori",
        "Khandallah", "Mākara", "Mākara Beach", "Ngaio", "Ngauranga", "Northland", "Wadestown", "Wilton", "Aotea",
        "Ascot Park", "Cannons Creek", "Elsdon", "Kenepuru", "Mana Island", "Porirua City Centre", "Rānui", "Takapūwāhia",
        "Tītahi Bay", "Waitangirua", "Camborne", "Hongoeka", "Judgeford", "Pukerua Bay", "Paekākāriki Hill", "Papakōwhai",
        "Paremata", "Pāuatahanui", "Plimmerton", "Whitby"
    ]
}

group_colors = {
    "Holy Family": "red",
    "St. Thomas": "blue",
    "St. Francis Xavier": "green",
    "St. Joseph’s": "orange",
    "Kapiti": "yellow",
    "St. Chavara": "purple",
    "Ocean": "lightblue",
    "St Alphonsa": "brown"
}

# Create a mapping from suburb name to color
def get_color(suburb_name):
    for group, suburbs in ward_groups.items():
        if suburb_name in suburbs:
            return group_colors[group]
    return "white" 

# -------------------------------------------
# Add GeoJSON layer with custom styling
# -------------------------------------------

folium.GeoJson(
    gdf,
    name="Suburbs",
    style_function=lambda feature: {
        'fillColor': get_color(feature['properties']['name']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6,
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Suburb:'])
).add_to(m)


legend_html = """
{% macro html(this, kwargs) %}

<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 200px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 14px;
    padding: 10px;
    ">
    <h4>Ward Colors</h4>
    <ul style="list-style: none; padding-left: 0;">
        <li><span style="background:red; width:15px; height:15px; display:inline-block;"></span> Holy Family</li>
        <li><span style="background:blue; width:15px; height:15px; display:inline-block;"></span> St. Thomas</li>
        <li><span style="background:green; width:15px; height:15px; display:inline-block;"></span> St. Francis Xavier</li>
        <li><span style="background:orange; width:15px; height:15px; display:inline-block;"></span> St. Joseph’s</li>
        <li><span style="background:yellow; width:15px; height:15px; display:inline-block;"></span> Kapiti</li>
        <li><span style="background:purple; width:15px; height:15px; display:inline-block;"></span> St. Chavara</li>
        <li><span style="background:brown; width:15px; height:15px; display:inline-block;"></span> St. Alphonsa</li>
    </ul>
</div>

{% endmacro %}
"""

legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

# Add suburb labels
for _, row in gdf.iterrows():
    folium.map.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                font-size: 8px; 
                color: black;
                background-color: rgba(255, 255, 255, 0);  /* fully transparent */
                padding: 0;
                border-radius: 0;
                white-space: nowrap;
                ">
                {row['name']}
            </div>
            """
        )
    ).add_to(m)



# Save or display
m.save("index.html")
m  # Display inline if using Jupyter

