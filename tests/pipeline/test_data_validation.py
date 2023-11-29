import pandas as pd
import pytest
from housing_price.pipeline.data_validation import DataValidation


# Define a fixture for creating an instance of DataValidation
@pytest.fixture
def data_validation_instance():
    return DataValidation()

# # Test case for values_from_schema method
# def test_values_from_schema(data_validation_instance, tmp_path):
#     # Create a temporary schema file for testing
#     schema_data = {'col_name': {'A': 'float', 'B': 'str'}, 'number_of_columns': 2}
#     schema_path = tmp_path / "schema_test.json"
#     with open(schema_path, 'w') as f:
#         json.dump(schema_data, f)
#
#     # Set the schema_path in the instance to the temporary file
#     data_validation_instance.schema_path = str(schema_path)
#
#     # Call the method
#     column_details, number_of_columns = data_validation_instance.values_from_schema()
#
#     # Assertions
#     assert column_details == {'A': 'float', 'B': 'str'}
#     assert number_of_columns == 2


# Test case for is_invalidate_column_length method
def test_is_invalidate_column_length(data_validation_instance):
    # Test data with a different number of columns than in the schema
    input_data = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z'], 'C': [4, 5, 6]})

    # Call the method
    result = data_validation_instance.is_invalidate_column_length(2, input_data)

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


def test_is_invalid_column_names(data_validation_instance):
    # Test data with invalid column names
    input_data = pd.DataFrame({'X': [1, 2, 3], 'Y': ['X', 'Y', 'Z']})

    # Call the method
    result, invalid_col_list = data_validation_instance.is_invalid_column_names({'A': 'float', 'B': 'str'}, input_data)

    # Assertions
    assert result is True  # Invalid column names
    assert invalid_col_list == {'X', 'Y'}  # Invalid columns


# Test case for is_invalid_data_type method
def test_is_invalid_data_type(data_validation_instance):
    # Test data with invalid data types
    input_data = pd.DataFrame({'A': [1.0, 2.0, 3.0], 'B': ['X', 'Y', 'Z']})

    # Call the method
    result, invalid_dtypes_column = data_validation_instance.is_invalid_data_type({'A': 'str', 'B': 'float'}, input_data)

    # Assertions
    assert result is True  # Invalid data types
    assert invalid_dtypes_column == ['A', 'B']  # Columns with invalid data types






