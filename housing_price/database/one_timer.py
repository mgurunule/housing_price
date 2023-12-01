from housing_price.constants.db_constants import (
    DB_NAME,
    TRANSFORMED_DATA_TABLE_NAME,
    PREDICTED_DATA_TABLE_NAME
)
from housing_price.database.db_operations import DataBaseOperation

from housing_price.test_logger import logger
import os

logger = logger.getChild(__name__)


path = os.getcwd().split("housing_price")[0] + "housing_price"


if __name__ == "__main__":

    try:
        # creating
        db_operations = DataBaseOperation(path, logger)
        # creating transformed db table
        db_operations.create_db_table(
            DB_NAME,
            TRANSFORMED_DATA_TABLE_NAME
            )
    except Exception as e:
        logger.error(f" Error in creating transformed table : {e}")
        raise

    try:
        # creating
        db_operations = DataBaseOperation(path, logger)
        # creating predicted db table
        db_operations.create_db_table(
            DB_NAME,
            PREDICTED_DATA_TABLE_NAME
            )
    except Exception as e:
        logger.error(f" Error in creating transformed table : {e}")
        raise





