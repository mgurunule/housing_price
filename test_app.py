import requests
import json
import pandas as pd
import pytest
import numpy as np


def api_url():
    return 'http://127.0.0.1:5001/predict'


def call_prediction_api(input_feature):

    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url(), data=json.dumps(input_feature), headers=headers)

    return response


def test_predict_endpoint_input_1():

    #  Sample input features :
    sample_input_1 = {'longitude': -122.64, 'latitude': 38.01, 'housing_median_age': 36.0,
                      'total_rooms': '1336.0', 'total_bedrooms': 258.0, 'population': 678.0,
                      'households': 249.0, 'median_income': 5.5789, 'ocean_proximity': 'NEAR OCEAN'
                      }

    response = call_prediction_api(sample_input_1)
    if response.status_code == 200:
        assert np.allclose(float(response.json()['MEDIAN_HOUSE_PRICE']), 320201.585540)


def test_predict_endpoint_input_2():

    sample_input_2 = {'longitude': -115.73, 'latitude': 33.35, 'housing_median_age': 23.0,
                      'total_rooms': '1586.0', 'total_bedrooms': 448.0, 'population': 338.0,
                      'households': 182.0, 'median_income': 1.2132, 'ocean_proximity': 'INLAND'
                      }

    response = call_prediction_api(sample_input_2)
    if response.status_code == 200:
        assert np.allclose(float(response.json()['MEDIAN_HOUSE_PRICE']), 58815.450338)


def test_predict_endpoint_input_3():

    sample_input_3 = {'longitude': -117.96, 'latitude': 33.89, 'housing_median_age': 24.0,
                      'total_rooms': '1332.0', 'total_bedrooms': 252.0, 'population': 625.0,
                      'households': 230.0, 'median_income': 4.4375, 'ocean_proximity': '<1H OCEAN'
                      }

    response = call_prediction_api(sample_input_3)
    if response.status_code == 200:
        assert np.allclose(float(response.json()['MEDIAN_HOUSE_PRICE']), 192575.773556)


def test_predict_endpoint_input_4():

    sample_input_4 = {'longitude': "Null", 'latitude': 33.89, 'housing_median_age': 24.0,
                      'total_rooms': '1332.0', 'total_bedrooms': 252.0, 'population': 625.0,
                      'households': 230.0, 'median_income': 4.4375, 'ocean_proximity': '<1H OCEAN'
                      }  # negative : Null value , so this will be dropped

    response = call_prediction_api(sample_input_4)
    print(response.json()['error message'])
    assert response.status_code == 999


def test_predict_endpoint_input_5():

    sample_input_5 = {'longitude': "Null", 'latitude': 33.89, 'housing_median_age': 24.0,
                      'total_rooms': '1332.0', 'total_bedrooms': 252.0, 'population': 625.0
                      }  # negative  # Schema mis-match

    response = call_prediction_api(sample_input_5)
    print(response.json()['error message'])
    assert response.status_code == 999

