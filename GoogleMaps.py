import time
from datetime import datetime
import numpy as np
import pandas as pd

import googlemaps

links = pd.read_csv('data/LinkOriginDestination.csv', sep = ';', names = ['LinkRef', 'FromLat', 'FromLng', 'ToLat', 'ToLng'])

api_key = ''
with open('api.key', 'r') as file:
    api_key = file.readline()

gmaps = googlemaps.Client(key=api_key)

with open('data/errors_' + datetime.now().date().isoformat() + '.csv', 'a') as error:
    with open('data/results_' + datetime.now().date().isoformat() + '.csv', 'a') as output:

        for index, row in links.iterrows():
            link_ref = row['LinkRef']
            origins = str(row['FromLat']) + ',' + str(row['FromLng'])
            destinations = str(row['ToLat']) + ',' + str(row['ToLng'])

            result = gmaps.distance_matrix(
                origins = origins,
                destinations = destinations,
                departure_time = datetime.now(),
                mode = 'driving',
                traffic_model = 'best_guess')

            if result['status'] == 'OK':
                cell = result['rows'][0]['elements'][0]
                output.write(datetime.now().isoformat() + ',' + link_ref + ',' + str(cell['distance']['value']) + ',' + str(cell['duration_in_traffic']['value']) + '\n')
            else:
                error.write(datetime.now().isoformat() + ',' + link_ref + ',' + result['status'] + '\n')
                
            time.sleep(5)