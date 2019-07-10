
import folium
import pandas as pd

data = pd.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <2000:
        return 'blue'
    elif 2000 <= elevation <3000:
        return 'red'
    else:
        return 'purple'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[35.306937, -80.735199],zoom_start=6)
fgv = folium.FeatureGroup(name="Volcanoes")

for lt,ln,el,name in zip(lat,lon,elev,name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt,ln],radius=6,popup=folium.Popup(iframe),fill_color=color_producer(el),color="grey",fill=True,fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json",'r',encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'blue' if x['properties']['POP2005']<10000000
else 'green' if x['properties']['POP2005']<20000000 else 'red' }))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")