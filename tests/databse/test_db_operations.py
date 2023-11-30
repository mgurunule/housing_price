import os
import pandas as pd
import pytest
from housing_price.database.db_operations import DataBaseOperation
from housing_price.test_logger import logger


logger = logger.getChild(__name__)

path = os.path.dirname(os.path.dirname(os.getcwd()))


# Define a fixture for creating an instance of DataBaseOperation
@pytest.fixture
def db_operation_instance():
    return DataBaseOperation(path=path, logger=logger)


# Test case for database_connection method
def test_database_connection(db_operation_instance):
    # Call the method
    result_conn = db_operation_instance.database_connection(database_name='test_db.db')

    # Assertions
    assert result_conn is not None  # Connection object should be created


# Test case for insert_into_table_transformed_data method
def test_insert_into_table(db_operation_instance):
    # Test data for insertion
    result_conn = db_operation_instance.database_connection(database_name='test_db.db')
    result_conn.execute("DROP TABLE IF EXISTS TestTable;")
    result_conn.commit()

    data = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})

    # Call the method
    db_operation_instance

    db_operation_instance.insert_into_table(database_name='test_db.db', data=data, table_name='TestTable')

    result_data = db_operation_instance.select_data_from_table(database_name='test_db.db', table_name='TestTable')

    pd.testing.assert_frame_equal(result_data, data, check_dtype=False)
