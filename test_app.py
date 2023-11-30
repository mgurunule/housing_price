import requests
import json
import pandas as pd
import pytest
import numpy as np

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


@pytest.fixture
def api_url():
    return 'http://127.0.0.1:5001/predict'


def test_predict_endpoint(api_url):

    sample_input_features = {'longitude': [-122.64, -115.73, -117.96],
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
    response = requests.post(api_url, data=json.dumps(sample_input_features), headers=headers)

    response_dataframe = pd.DataFrame(response.json())

    assert response.status_code == 200
    assert 'MEDIAN_HOUSE_PRICE' in response_dataframe.columns.tolist()
    assert np.allclose(response_dataframe['MEDIAN_HOUSE_PRICE'].values, [320201.585540, 58815.450338, 192575.773556])