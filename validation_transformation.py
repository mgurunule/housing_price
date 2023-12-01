from datetime import datetime
from housing_price.constants.common_constants import (
    COLUMN_FOR_ENCODING,
    COLUMNS_FOR_MODEL,
    OBJ_TO_FLOAT_COL,
    RENAMING_COL_FOR_DB,
)
from housing_price.constants.db_constants import (
    DB_NAME,
    TRANSFORMED_DATA_TABLE_NAME
)
import pandas as pd
from housing_price.logger import logger
from housing_price.database.db_operations import DataBaseOperation
from housing_price.pipeline.data_transformation import DataTransformation
from housing_price.pipeline.data_validation import DataValidation


def load_logger():
    logging = logger.getChild(__name__)
    return logging


class ValidationTransformation:
    def __init__(self, path, ):
        self.logger = load_logger()
        self.path = path
        self.raw_data = DataValidation(path, self.logger)
        self.data_transform = DataTransformation(self.logger)
        self.db_operations = DataBaseOperation(path, self.logger)

    def perform_validation_transformation(self, input_data: pd.DataFrame
                                          ) -> pd.DataFrame:

        """
        Description: This method performs the basic validation and
                     transformation steps before giving this
                     data to the model
        Parameters
        ----------
        input_data:  raw input data from api

        Returns
        -------
        pd.DataFrame
            transformed data
        """
        try:
            #############################################################
            # ------------------   DATA VALIDATION ---------------------
            self.logger.info(" Start the Validation of Raw data")
            input_value_for_logger = ""

            for col in input_data.columns:
                columns_value = f" {col} : {input_data.loc[0,col]} ,"
                input_value_for_logger = input_value_for_logger + columns_value

            self.logger.info(input_value_for_logger)
            # 1 extracting value from prediction schema
            column_details, number_of_columns = self.raw_data.\
                values_from_schema()

            # 2 Validation the column length
            if self.raw_data.is_invalid_column_length(
                    number_of_columns,
                    input_data):
                self.logger.error(" Invalid column length "
                                  "of the input dataframe ")
                return
            self.logger.info(" column length of input "
                             "dataframe matched with schema")

            # 3 validate if any column has complete missing values

            invalid_column_names, invalid_col_list = self.raw_data.\
                is_invalid_column_names(column_details, input_data)
            if invalid_column_names:
                self.logger.error(f" Invalid columns : {invalid_col_list}")
                return 
            self.logger.info(" Valid column name in input data")

            input_data = self.raw_data.convert_column_type(input_data, OBJ_TO_FLOAT_COL)

            nan_invalid_values, nan_invalid_columns = self.raw_data.\
                is_nan_present(input_data)
            if nan_invalid_values:
                self.logger.error(f" Invalid values for columns : {nan_invalid_columns} ")
                return

            invalid_dtypes, invalid_dtypes_column = self.raw_data.\
                is_invalid_data_type(column_details, input_data)
            if invalid_dtypes:
                self.logger.error(f" INVALID data type "
                                  f"for {invalid_dtypes_column}")
                return 

            self.logger.info(" Data Validation done , "
                             "Data Transformation started")

            #############################################################
            # ------------------   DATA TRANSFORMATION  ---------------------

            # transformed_data = self.data_transform.drop_missing_values(
            #                             input_data)

            # if transformed_data.empty:
            #     self.logger.error(" Empty dataframe, "
            #                       "records cannot be processed further")
            #     return

            transformed_data = self.data_transform.perform_encoding(
                input_data, COLUMN_FOR_ENCODING)

            transformed_data = self.data_transform.\
                add_missing_column_after_encoding(transformed_data)

            # For some model order of columns matters so re-arranging
            # columns before giving to model
            transformed_data = transformed_data.loc[:, COLUMNS_FOR_MODEL]

            self.logger.info(" Re-arranging columns done")
            # columns name contain > and space which is not allowed in
            # databse, so re-naming them

            transformed_data.rename(columns=RENAMING_COL_FOR_DB, inplace=True)
            self.logger.info(" Re-naming columns for databse done")
            self.logger.info(" Data transformation done")

            #############################################################
            table_data = transformed_data.copy()
            # ------------------   SAVE TRANSFORMED DATA To DATABASE  ---
            table_data['event_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.db_operations.insert_into_table(
                                        DB_NAME,
                                        table_data,
                                        TRANSFORMED_DATA_TABLE_NAME
                                        )

            return transformed_data

        except Exception as e:
            self.logger.error(" Error in Prediction validation")
            raise e
