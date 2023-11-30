import json
import os
import pandas as pd
import pytest
from housing_price.pipeline.data_validation import DataValidation
from housing_price.test_logger import logger

logger = logger.getChild(__name__)

path = os.path.dirname(os.path.dirname(os.getcwd()))


# Define a fixture for creating an instance of DataValidation
@pytest.fixture
def data_validation_instance():
    return DataValidation(path, logger)


# Test case for values_from_schema method
def test_values_from_schema(data_validation_instance, tmp_path):
    # Create a temporary schema file for testing
    schema_data = {'col_name': {'A': 'float', 'B': 'str'}, 'number_of_columns': 2}
    schema_path = tmp_path / "schema_test.json"
    with open(schema_path, 'w') as f:
        json.dump(schema_data, f)

    # Set the schema_path in the instance to the temporary file
    data_validation_instance.schema_path = str(schema_path)

    # Call the method
    column_details, number_of_columns = data_validation_instance.values_from_schema()

    # Assertions
    assert column_details == {'A': 'float', 'B': 'str'}
    assert number_of_columns == 2


# Test case for is_invalidate_column_length method
def test_is_invalidate_column_length(data_validation_instance):
    # Test data with a different number of columns than in the schema
    input_data = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z'], 'C': [4, 5, 6]})

    # Call the method
    result = data_validation_instance.is_invalid_column_length(2, input_data)

    # Assertion
    assert result is True  # Number of columns mismatch


# Test case for is_having_missing_values method
def test_is_having_missing_values(data_validation_instance):
    # Test data with missing values
    input_data = pd.DataFrame({'A': [1, 2, 4], 'B': [None, None, None], 'C': [4, 5, 6]})

    # Call the method
    result, missing_columns = data_validation_instance.is_having_missing_values(input_data)

    # Assertions
    assert result is True  # Missing values present
    assert missing_columns == ['B']  # Columns with missing values


def test_is_invalid_column_names_false(data_validation_instance):
    # Test data with invalid column names

    valid_columns_details = {"longitude": "float",
                             "latitude": "float",
                             "housing_median_age": "float",
                             "total_rooms": "float",
                             "total_bedrooms": "float",
                             "population": "float",
                             "households": "float",
                             "median_income": "float",
                             "ocean_proximity": "str"
                            }
    input_data = pd.DataFrame({'longitude': [-122.64, -115.73, -117.96],
                               'latitude': [38.01, 33.35, 33.89],
                               'housing_median_age': [36.0, 23.0, 24.0],
                               'total_rooms': [1336.0, 1586.0, 1332.0],
                               'total_bedrooms': [258.0, 448.0, 252.0],
                               'population': [678.0, 338.0, 625.0],
                               'households': [249.0, 182.0, 230.0],
                               'median_income': [5.5789, 1.2132, 4.4375],
                               'ocean_proximity': ['NEAR OCEAN', 'INLAND', '<1H OCEAN']
                               }
                              )

    # Call the method
    result, invalid_col_list = data_validation_instance.is_invalid_column_names(valid_columns_details, input_data)

    # Assertions
    assert result is False  # Invalid column names
    assert invalid_col_list == []  # Invalid columns


def test_is_invalid_column_names_true(data_validation_instance):
    # Test data with invalid column names

    valid_columns_details = {"longitude": "float",
                             "latitude": "float",
                             "housing_median_age": "float",
                             "total_rooms": "float",
                             "total_bedrooms": "float",
                             "population": "float",
                             "households": "float",
                            }
    input_data = pd.DataFrame({'longitude': [-122.64, -115.73, -117.96],
                               'latitude': [38.01, 33.35, 33.89],
                               'housing_median_age': [36.0, 23.0, 24.0],
                               'total_rooms': [1336.0, 1586.0, 1332.0],
                               'total_bedrooms': [258.0, 448.0, 252.0],
                               'population': [678.0, 338.0, 625.0],
                               'households': [249.0, 182.0, 230.0],
                               'median_income': [5.5789, 1.2132, 4.4375],
                               'ocean_proximity': ['NEAR OCEAN', 'INLAND', '<1H OCEAN']
                               }
                              )
    # Call the method
    result, invalid_col_list = data_validation_instance.is_invalid_column_names(valid_columns_details, input_data)

    # Assertions
    assert result is True  # Invalid column names
    assert sorted(invalid_col_list) == sorted(['median_income', 'ocean_proximity'])  # Invalid columns


# Test case for is_invalid_data_type method
def test_is_invalid_data_type(data_validation_instance):
    # Test data with invalid data types
    input_data = pd.DataFrame({'A': [1.0, 2.0, 3.0], 'B': ['X', 'Y', 'Z']})

    # Call the method
    result, invalid_dtypes_column = data_validation_instance.is_invalid_data_type({'A': 'str', 'B': 'float'}, input_data)

    # Assertions
    assert result is True  # Invalid data types
    assert invalid_dtypes_column == ['A', 'B']  # Columns with invalid data types






