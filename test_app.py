import requests
import json

api_url =  'http://127.0.0.1:5000/predict'


# def test_end_point():

test_data = {'longitude': [-122.64, -115.73, -117.96],
             'latitude': [38.01, 33.35, 33.89],
             'housing_median_age': [36.0, 23.0, 24.0],
             'total_rooms': [1336.0, 1586.0, 1332.0],
             'total_bedrooms': [258.0, 448.0, 252.0],
             'population': [678.0, 338.0, 625.0],
             'households': [249.0, 182.0, 230.0],
             'median_income': [5.5789, 1.2132, 4.4375],
             'ocean_proximity': ['NEAR OCEAN', 'INLAND', '<1H OCEAN']
             }

headers = {'Content-Type': 'application/json'}
response = requests.post("http://127.0.0.1:5001/predict", data=json.dumps(test_data), headers=headers)
print(response.content)
