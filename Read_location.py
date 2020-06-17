# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:16:05 2020

@author: rikis
"""

import json
from pandas import DataFrame

file = open('D:/URBAG/Frost/locations.txt', 'r', encoding='utf-8')

my_json_string = file.read()

to_python = json.loads(my_json_string)


names = []
lat = []
lon = []

for i in range(len(to_python['data'])):
    names.append(to_python['data'][i]['name'])
    lat.append(to_python['data'][i]['geometry']['coordinates'][1])
    lon.append(to_python['data'][i]['geometry']['coordinates'][0])
    


my_dataframe = DataFrame()
my_dataframe['Name'] = names
my_dataframe['Latitude'] = lat
my_dataframe['Longitude'] = lon


print(my_dataframe)
my_dataframe.to_csv('Locations.csv',encoding='iso-8859-1')
