import pandas as pd
import pytest
from housing_price.pipeline.data_transformation import DataTransformation


# Define a fixture for creating an instance of DataTransformation
@pytest.fixture
def data_transformation_instance():
    return DataTransformation()


# Test case for drop_missing_values method
def test_drop_missing_values(data_transformation_instance):
    # Test data with missing values
    input_data = pd.DataFrame({'A': [1, 2, None, 4], 'B': ['X', 'Y', 'Z', "Null"]})

    # Call the method
    result_data = data_transformation_instance.drop_missing_values(input_data)

    # Assertions
    assert result_data.shape[0] == 2  # Two rows with complete data
    assert 'Null' not in result_data.values  # No 'Null' values in the DataFrame


# # Test case for add_missing_column_after_encoding method
# def test_add_missing_column_after_encoding(data_transformation_instance):
#     # Test data with missing columns
#     input_data = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z']})
#
#     # Call the method
#     result_data = data_transformation_instance.add_missing_column_after_encoding(input_data)
#
#     # Assertions
#     assert 'Encoded_Column_1' in result_data.columns  # Assuming 'Encoded_Column_1' is a missing column
#     assert result_data['Encoded_Column_1'].all() == 0  # All values in the missing column should be 0


def test_perform_encoding(data_transformation_instance):
    # Test data for encoding
    input_data = pd.DataFrame({'Category': ['A', 'B', 'A', 'C']})

    # Call the method
    result_data = data_transformation_instance.perform_encoding(input_data, ['Category'])

    # Assertions
    assert 'Category_A' in result_data.columns  # Check for the presence of encoded columns
    assert 'Category_B' in result_data.columns
    assert 'Category_C' in result_data.columns
    assert list(result_data['Category_A'].values) == [1, 0, 1, 0]  # Check encoding correctness

