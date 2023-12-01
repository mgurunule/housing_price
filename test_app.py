import requests
import json
import pandas as pd
import pytest
import numpy as np

# test_data = {'longitude': [-122.64, -115.73, -117.96],
#              'latitude': [38.01, 33.35, 33.89],
#              'housing_median_age': [36.0, 23.0, 24.0],
#              'total_rooms': [1336.0, 1586.0, 1332.0],
#              'total_bedrooms': [258.0, 448.0, 252.0],
#              'population': [678.0, 338.0, 625.0],
#              'households': [249.0, 182.0, 230.0],
#              'median_income': [5.5789, 1.2132, 4.4375],
#              'ocean_proximity': ['NEAR OCEAN', 'INLAND', '<1H OCEAN']
#              }
# sample_input_features_1 = {'longitude': [-122.64],
#                            'latitude': [38.01],
#                            'housing_median_age': [36.0],
#                            'total_rooms': ['1336.0'],
#                            'total_bedrooms': [258.0],
#                            'population': [678.0],
#                            'households': [249.0],
#                            'median_income': [5.5789],
#                            'ocean_proximity': ['NEAR OCEAN']
#                            }
#
# sample_input_features_2 = {'longitude': [-115.73],
#                            'latitude': [33.35],
#                            'housing_median_age': [23.0],
#                            'total_rooms': ['1586.0'],
#                            'total_bedrooms': [448.0],
#                            'population': [338.0],
#                            'households': [182.0],
#                            'median_income': [1.2132],
#                            'ocean_proximity': ['INLAND']
#                            }
# sample_input_features_3 = {'longitude': [-117.96],
#                            'latitude': [33.89],
#                            'housing_median_age': [24.0],
#                            'total_rooms': ['1332.0'],
#                            'total_bedrooms': [252.0],
#                            'population': [625.0],
#                            'households': [230.0],
#                            'median_income': [4.4375],
#                            'ocean_proximity': ['<1H OCEAN']
#                            }


@pytest.fixture
def api_url():
    return 'http://127.0.0.1:5001/predict'


def test_predict_endpoint(api_url):

#    Sample input features :
    sample_input_1 = {'longitude': -122.64, 'latitude': 38.01, 'housing_median_age': 36.0,
                      'total_rooms': '1336.0', 'total_bedrooms': 258.0, 'population': 678.0,
                      'households': 249.0, 'median_income': 5.5789, 'ocean_proximity': 'NEAR OCEAN'
                      }

    sample_input_2 = {'longitude': -115.73, 'latitude': 33.35, 'housing_median_age': 23.0,
                      'total_rooms': '1586.0', 'total_bedrooms': 448.0, 'population': 338.0,
                      'households': 182.0, 'median_income': 1.2132, 'ocean_proximity': 'INLAND'
                      }
    sample_input_3 = {'longitude': -117.96, 'latitude': 33.89, 'housing_median_age': 24.0,
                      'total_rooms': '1332.0', 'total_bedrooms': 252.0, 'population': 625.0,
                      'households': 230.0, 'median_income': 4.4375, 'ocean_proximity': '<1H OCEAN'
                      }
    sample_input_4 = {'longitude': "Null", 'latitude': 33.89, 'housing_median_age': 24.0,
                      'total_rooms': '1332.0', 'total_bedrooms': 252.0, 'population': 625.0,
                      'households': 230.0, 'median_income': 4.4375, 'ocean_proximity': '<1H OCEAN'
                      }  # negative : Null value , so this will be dropped
    sample_input_5 = {'longitude': "Null", 'latitude': 33.89, 'housing_median_age': 24.0,
                      'total_rooms': '1332.0', 'total_bedrooms': 252.0, 'population': 625.0
                      }  # negative  # Schema mis-match

    sample_inputs = [sample_input_1, sample_input_2, sample_input_3,
                     sample_input_4, sample_input_5]


    headers = {'Content-Type': 'application/json'}

    for inputs in sample_inputs:
        response = requests.post(api_url, data=json.dumps(inputs), headers=headers)
        if response.status_code == 200:
            response_dataframe = pd.DataFrame(response.json())

            assert 'MEDIAN_HOUSE_PRICE' in response_dataframe.columns.tolist()

         #   assert np.allclose(response_dataframe['MEDIAN_HOUSE_PRICE'].values, [320201.585540, 58815.450338, 192575.773556])
        else:
            print("Error occured")
