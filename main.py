from turtle import fillcolor
import folium
import pandas
from geopy.geocoders import Nominatim
from haversine import haversine
import argparse
import csv 
import random
from ast import literal_eval as make_tuple

mxloc = 10



def create_map(path, me, locs, locs2):

    loc_list = list(locs.keys())
    loc_list.sort(key = lambda x: haversine(me, locs[x]))
    loc_list_first_10 = loc_list[:mxloc]

    map = folium.Map(location=list(me), zoom_start=10)
    map.add_child(folium.CircleMarker(location=list(me), popup="Your location",fill_color = "green", fill_opacity = 1))


    fg = folium.FeatureGroup(name = 'Ten clothest locations')
    for x in loc_list_first_10:
        fg.add_child(folium.Marker(location=list(locs[x]), popup=x, icon=folium.Icon()))
    map.add_child(fg)

    fg2 = folium.FeatureGroup(name = 'Some other locations')
    for x in locs2:
        fg2.add_child(folium.CircleMarker(location=list(locs2[x]), radius=10, popup=x, fill_color="red", fill_opacity=1))
    map.add_child(fg2)

    map.save(path)


def f(s):
    x = []
    for i in range(len(s)):
        if s[i] == ',':
            x.append(i)
    name = s[2:x[0]-1]
    year = s[x[0] + 3 : x[1] - 1]
    loc = s[x[1]+ 3 : -3]
    return (name, year,loc)


def read_from_file():
    locs = []
    reader = open('locs.txt', 'r')
    for row in reader:
        locs.append(f(row))
    return locs

if __name__ == '__main__':


    locs = read_from_file()

    parser = argparse.ArgumentParser(description="Creating map for movies filmed certain year")
    parser.add_argument('year',type=int)
    parser.add_argument('latitude',type=float)
    parser.add_argument('longtitude',type=float)
    parser.add_argument('path',type=str)

    args = parser.parse_args()


    locs_this_year = []
    for (x,y,z) in locs:
        if y == str(args.year):
            locs_this_year.append((x,z))

    random.shuffle(locs_this_year)

    coord = {}
    geolocator = Nominatim(user_agent="Map creator")
    for (x, y) in locs_this_year:
        if len(coord) >= mxloc:
            break
        location = geolocator.geocode(y)
        if location is not None:
            coord[x] = (location.latitude, location.longitude)

    random.shuffle(locs)
    coord2 = {}
    for (x, _, y) in locs:
        if len(coord2) >= mxloc:
            break
        location = geolocator.geocode(y)
        if location is not None:
            coord2[x] = (location.latitude, location.longitude)


    create_map(args.path, (args.latitude, args.longtitude), coord, coord2)