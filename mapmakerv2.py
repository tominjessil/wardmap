import geopandas as gpd
import folium
from folium import Element
import leafmap.foliumap as leafmap

gsdf = gpd.read_file("nz-suburbs.geojson") # Less detailed original
# gsdf = gpd.read_file("detailed_boundaries_with_names.geojson")

ward_suburbs = {
    "Holy Family": ["Avalon", "Belmont", "Boulcott", "Epuni", "Harbour View", "Kelson", "Tirohanga"],
    "St.Thomas": ["Petone", "Eastbourne", "Naenae", "Korokoro", "Waiwhetū", "Woburn", "Waterloo",
                   "Hutt Central", "Wainuiomata", "Seaview", "Alicetown"],
    "St.Francis Xavier": ["Stokes Valley", "Taitā", "Manor Park"],
    "St.Joseph’s": ["Silverstream", "Pinehaven", "Blue Mountains", "Heretaunga", "Trentham",
                     "Riverstone Terraces", "Haywards", "Wallaceville", "Elderslea", "Ebdentown",
                     "Whit  emans Valley", "Kingsley Heights", "Clouston Park", "Tōtara Park",
                     "Maoribank", "Brown Owl", "Mangaroa", "Timberlea", "Birchville", "Te Mārua",
                     "Kaitoke", "Akatarawa"],
    "Kapiti": ["Raumati Beach", "Raumati South", "Maungakōtukutuku", "Paraparaumu",
               "Paraparaumu Beach", "Otaihanga", "Waikanae", "Waikanae Beach",
               "Peka Peka", "Reikorangi"],
    "St.Chavara": ["Miramar", "Kilbirnie", "Island Bay", "Berhampore", "Newtown", "Brooklyn",
                    "Aro Valley", "Mount Cook", "Kelburn", "Thorndon", "Hataitai"],
    "St.Alphonsa": ["Tawa", "Churton Park", "Glenside", "Grenada North", "Grenada Village",
                    "Horokiwi", "Johnsonville", "Newlands", "Ohariu", "Paparangi", "Takapu Valley",
                    "Woodridge", "Broadmeadows", "Crofton Downs", "Kaiwharawhara", "Karori",
                    "Khandallah", "Mākara", "Mākara Beach", "Ngaio", "Ngauranga", "Northland",
                    "Wadestown", "Wilton", "Aotea", "Ascot Park", "Cannons Creek", "Elsdon",
                    "Kenepuru", "Mana Island", "Porirua City Centre", "Rānui", "Takapūwāhia",
                    "Tītahi Bay", "Waitangirua", "Camborne", "Hongoeka", "Judgeford", "Pukerua Bay",
                    "Paekākāriki Hill", "Papakōwhai", "Paremata", "Pāuatahanui", "Plimmerton", "Whitby",
                    "Wadestown"]
}

ward_colours = {
    "Holy Family": "#e6194b",     
    "St.Thomas": "#4363d8",      
    "St.Francis Xavier": "#73cd85",  
    "St.Joseph’s": "#f58231",    
    "Kapiti": "#cec93e",         
    "St.Chavara": "#911eb4",     
    "St.Alphonsa": "#b27b53"      
}

def get_ward_colour(ward):
    if ward_colours.get(ward) == None:
        return "#ffffff"
    return ward_colours[ward]

def get_ward_name(suburb):
    for ward, suburbs in ward_suburbs.items():
        if suburb in suburbs:
            return ward
    return ""
   
gsdf["ward"] = gsdf["name"].apply(get_ward_name)
gsdf["fill"] = gsdf["ward"].apply(get_ward_colour)
gsdf["fill-opacity"] = 0.45
gsdf["stroke"] = "#555555"
gsdf["stroke-width"] = 1
gsdf["stroke-opacity"] = 1
gsdf.to_file("suburbs_coloured.geojson", driver="GeoJSON") 

f_map = folium.Map(location=[-41.2, 174.8], zoom_start=10, tiles="Cartodb Positron")

popup = folium.GeoJsonPopup(
    fields=["name", "ward"],
    aliases=["Suburb", "Ward"],
    localize=True,
    labels=True,
    style="background-color: rgba(0,0,0,0);",
)

tooltip = folium.GeoJsonTooltip(
    fields=["name", "ward"],
    aliases=["Suburb:", "Ward:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

folium.GeoJson("suburbs_coloured.geojson",
                name = "St Mary's Syro Malabar Wards",
                style_function=lambda feature: {
                    "fillColor": feature["properties"]["fill"],
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.45,
                    "opacity": 1
                },
                tooltip=tooltip,
                popup=popup,
            ).add_to(f_map)

folium.TileLayer("Cartodb Positron", overlay=False, control=True, show=True).add_to(f_map)
folium.TileLayer("OpenStreetMap", overlay=False, control=True, show=False).add_to(f_map)
folium.LayerControl().add_to(f_map)

legend_html = '''
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
    <i style="background:#4363d8; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St.Thomas<br>
    <i style="background:#73cd85; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St.Francis Xavier<br>
    <i style="background:#f58231; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St.Joseph’s<br>
    <i style="background:#cec93e; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> Kapiti<br>
    <i style="background:#911eb4; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St.Chavara<br>
    <i style="background:#b27b53; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> St.Alphonsa<br>
</div>
''' 

f_map.get_root().html.add_child(folium.Element(legend_html))

f_map.save('index.html')

