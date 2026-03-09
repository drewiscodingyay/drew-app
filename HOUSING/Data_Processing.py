import folium
import pandas as pd
import requests
from folium.plugins import TimeSliderChoropleth
import branca.colormap as cm

# Load data
df = pd.read_csv("HOUSING/share living with parents.csv")
countries = ['Spain', 'Italy', 'Greece', 'Portugal', 'Denmark', 'Finland', 'Sweden']

df = df[df['geo'].isin(countries)]
df = df[df['wstatus'] == 'Employed persons working full-time']
df = df[df['TIME_PERIOD'].between(2015, 2024)]
df = df[['geo', 'TIME_PERIOD', 'OBS_VALUE']].dropna()

# Download GeoJSON
url = "https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"
geo_data = requests.get(url).json()
geo_data['features'] = [
    f for f in geo_data['features']
    if f['properties']['NAME'] in countries
]

# Add id to each feature
for i, feature in enumerate(geo_data['features']):
    feature['id'] = str(i)

# Build colormap
min_val = df['OBS_VALUE'].min()
max_val = df['OBS_VALUE'].max()
colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)

# Build style dict using feature id as key
style_dict = {}

for feature in geo_data['features']:
    fid = feature['id']
    name = feature['properties']['NAME']
    country_data = df[df['geo'] == name].sort_values('TIME_PERIOD')
    style_dict[fid] = {}
    for _, row in country_data.iterrows():
        year = int(row['TIME_PERIOD'])
        epoch = str(int(pd.Timestamp(f"{year}-01-01").timestamp()))
        color = colormap(row['OBS_VALUE'])
        style_dict[fid][epoch] = {'color': color, 'opacity': 0.9}

# Create map
m = folium.Map(location=[54, 12], zoom_start=4, tiles="CartoDB positron")

TimeSliderChoropleth(
    data=geo_data,
    styledict=style_dict,
).add_to(m)

colormap.caption = 'Share Living with Parents - Full Time Employed 25-34 (%)'
colormap.add_to(m)

m.save("HOUSING/map.html")
print("Map saved!")