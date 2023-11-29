from housing_price.constants.common_constants import (
    COLUMN_FOR_ENCODING,
    COLUMNS_FOR_MODEL,
    RENAMING_COL_FOR_DB,
)
from housing_price.constants.db_constants import (
    DB_NAME,
    TRANSFORMED_DATA_TABLE_NAME
)
import pandas as pd
from housing_price.database.db_operations import DataBaseOperation
from housing_price.pipeline.data_transformation import DataTransformation
from housing_price.pipeline.data_validation import DataValidation


class ValidationTransformation:
    def __init__(self, path, logger):
        self.path = path
        self.raw_data = DataValidation(path, logger)
        self.data_transform = DataTransformation(logger)
        self.db_operations = DataBaseOperation(path, logger)
        self.logger = logger

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
            missing_values, missing_columns = self.raw_data.\
                is_having_missing_values(input_data)
            if missing_values:
                self.logger.error(f" Missing value in {missing_columns}")
                return

            self.logger.info(" No complete missing column found")

            invalid_column_names, invalid_col_list = self.raw_data.\
                is_invalid_column_names(column_details, input_data)
            if invalid_column_names:
                self.logger.error(f" Invalid columns : {invalid_col_list}")
                return
            self.logger.info(" Valid column name in input data")

            invalid_dtypes, invalid_dtypes_column = self.raw_data.\
                is_invalid_data_type(column_details, input_data)
            if invalid_dtypes:
                self.logger.error(f" INVALID data type "
                                  f"for {invalid_dtypes_column}")

            self.logger.info(" Data Validation done , "
                             "Data Transformation started")

            #############################################################
            # ------------------   DATA TRANSFORMATION  ---------------------

            transformed_data = self.data_transform.drop_missing_values(
                                        input_data)

            if transformed_data.empty:
                self.logger.error(" Empty dataframe, "
                                  "records cannot be processed further")

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
            # ------------------   SAVE TRANSFORMED DATA To DATABASE  ---

            # this should be one timer

            self.db_operations.create_db_table(
                                        DB_NAME,
                                        TRANSFORMED_DATA_TABLE_NAME
                                        )

            self.db_operations.insert_into_table(
                                        DB_NAME,
                                        transformed_data,
                                        TRANSFORMED_DATA_TABLE_NAME
                                        )

            # THIS is to fetch the transformed record from databse
            # this is not required for now
            # fetched_data = self.db_operations.select_data_from_table(
            #                             DB_NAME,
            #                             TRANSFORMED_DATA_TABLE_NAME
            #                             )
            return transformed_data

        except Exception as e:
            self.logger.error(" Error in Prediction validation")
            raise e
