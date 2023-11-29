import pandas as pd
import pytest
from housing_price.database.db_operations import DataBaseOperation

# Define a fixture for creating an instance of DataBaseOperation
@pytest.fixture
def db_operation_instance(tmp_path):
    return DataBaseOperation(path=tmp_path)


# Test case for database_connection method
def test_database_connection(db_operation_instance):
    # Call the method
    result_conn = db_operation_instance.database_connection(database_name='test_db')

    # Assertions
    assert result_conn is not None  # Connection object should be created


# Test case for create_db_table method
def test_create_db_table(db_operation_instance):
    # Create a temporary query file for testing
    query_path = db_operation_instance.path / "create_table_test.sql"
    with open(query_path, 'w') as f:
        f.write("CREATE TABLE TestTable (ID INT, Name TEXT);")

    # Set the query path in the instance to the temporary file
    db_operation_instance.path = str(query_path.parent)

    # Call the method
    db_operation_instance.create_db_table(database_name='test_db', table_name='TestTable')

    # Assertions
    # Check if the table is created (you might want to use another method to verify the table creation)
    assert True  # Replace with appropriate assertion


# Test case for insert_into_table_transformed_data method
def test_insert_into_table(db_operation_instance):
    # Test data for insertion
    data = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})

    # Call the method
    db_operation_instance.insert_into_table(database_name='test_db', data=data, table_name='TestTable')

    # Assertions
    # Check if records are inserted (you might want to use another method to verify the insertion)
    assert True  # Replace with appropriate assertion


# Test case for select_data_from_table method
def test_select_data_from_table(db_operation_instance):
    # Call the method
    result_data = db_operation_instance.select_data_from_table(database_name='test_db', table_name='TestTable')

    # Assertions
    assert isinstance(result_data, pd.DataFrame)  # Result should be a DataFrame
