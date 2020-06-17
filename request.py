# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:16:37 2020

@author: rikis
"""

import requests
import pandas as pd
import json

client_id = '1416f8f1-da7b-4675-9bde-55ba9b2654b9'

# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'

def request_source(source):
    parameters = {
        'sources': source,
        'elements': 'air_temperature,wind_speed, wind_from_direction',
        'referencetime': '2015-06-01/2015-07-01',
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id,''))
    # Extract JSON data
    json = r.json()

    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])
        print(source)
        return 0

    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]['observations'])
        row['referenceTime'] = data[i]['referenceTime']
        row['sourceId'] = data[i]['sourceId']
        df = df.append(row)

    df = df.reset_index()
    print('Now df2')
    columns = ['sourceId','referenceTime','level', 'elementId','value','unit','timeOffset']
    df2 = df[columns].copy()
    Height = []

    print('collect heights')
    for index, row in df2.iterrows():
        Height.append(row['level']['value'])
    df2['Height'] = Height
    
    print('remove T10')
    # Convert the time value to something Python understands
    df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

    df2 = df2.drop(df2[(df2['elementId'] == 'air_temperature') & (df2['Height'] == 10)].index)

    df2.to_csv('./Obs/'+source+'.csv',encoding='utf-8' )
    return 1


sources = ['SN18700','SN18269','SN18260','SN18245','SN18230','SN18170','SN18215',\
 'SN18233','SN18980','SN18020','SN18310','SN18920','SN18690','SN18645','SN18205',\
 'SN18950','SN18235','SN18420','SN18160','SN18815','SN18315','SN18405','SN18701',\
 'SN18450','SN18390','SN18240','SN17980','SN18195','SN18500','SN18180','SN18270',\
 'SN18162','SN18440','SN18225','SN18165','SN18210','SN18703','SN18670','SN18410']

for source in sources:
    request_source(source)




