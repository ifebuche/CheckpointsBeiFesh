import pandas as pd
import re, folium
import matplotlib.pyplot as plt

#Read txt data file 
with open("WhatsApp Chat with Ifebu m.txt", "r", encoding = "utf-8") as file:
    chats = file.readlines()
print(len(chats))

#Isolate all lines with string 'location' and the last split element starts with https
locations = [line.split()[-1] for line in chats if 'location' in line and line.split()[-1].startswith('https')]

lats, lons, pops = [], [], []
for item in locations[25:]:
    pops.append(item)
    #get the last 19 digits as it covers the longest lat_lon entry length, split at the comma
    item = item[-19:].split(',')
    #take the numbers (starts with a digit followed by a period and digits) from first split item
    #join() to convert to string from list in order to convert to float and save as lat
    latitude = float(''.join(re.findall("\d[.]\d+", item[0])))
    #convert second split item to long after converting with join() to a string
    longitude = float(''.join(item[1]))
    lats.append(latitude)
    lons.append(longitude)
    #print(item[0], float(''.join(lat)))

print("Making file...")
with open("points.csv", "w") as file:
    for lat,lon in zip(lats, lons):
        file.write(str(lat) + ', ' + str(lon) + '\n')
        
points = pd.read_csv("points.csv", header=None)
points.columns = ['lon', 'lat']
points.head()
        
fesh_map = folium.Map(location=[float(locations[-1][-19:][:9]), float(locations[-1][-19:][-9:])],
                        zoom_start=9,
                        radius=95,
                        color="#E37222",
                        fill=True, 
                     tiles = "openstreetmap")
folium.TileLayer('stamenterrain', attr="<a href=https://deparkes.co.uk/2016/06/10/folium-map-tiles/>Endless Sky</a>").add_to(fesh_map)
folium.TileLayer('cartodbpositron', attr="<a href=https://deparkes.co.uk/2016/06/10/folium-map-tiles/>Endless Sky</a>").add_to(fesh_map)
folium.TileLayer('cartodbdark_matter', attr="<a href=https://deparkes.co.uk/2016/06/10/folium-map-tiles/>Endless Sky</a>").add_to(fesh_map)
folium.LayerControl().add_to(fesh_map)

for lat,lon, pop in zip(lats, lons, pops):
    folium.Marker(location=[lat, lon], popup=pop, tooltip="Click for Google Maps link").add_to(fesh_map)

#Show the map
fesh_map

#Save the map as html
fesh_map.save("CheckpointsByFesh.html")