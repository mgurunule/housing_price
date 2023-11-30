import os
import json
from housing_price.constants.common_constants import (
    COL_NAME,
    NUMBER_OF_COLUMNS,
    SCHEMA_FILE,
)
import pandas as pd


class DataValidation:
    """
        This class shall be used for handling all the validation done
        on the raw Prediction Detail.
    """
    def __init__(self, path, logger):
        self.schema_path = os.path.join(path, SCHEMA_FILE)
        self.logger = logger

    def values_from_schema(self) -> tuple[dict, int]:
        """
            Description: read the values from schema file
                        and return the details
        Returns
        -------
            column_details :  valid column names and types
            number_of_columns : length of valid columns
        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            column_details = dic[COL_NAME]
            number_of_columns = dic[NUMBER_OF_COLUMNS]

            self.logger.info(" Schema details retrieved from Schema json")

        except Exception as e:
            self.logger.error(" Error in fetching schema details")
            raise e

        return column_details, number_of_columns

    def is_invalid_column_length(self,
                                 number_of_columns: int,
                                 input_data: pd.DataFrame) -> bool:
        """
            Description: This function verify if the number of columns of
                         input dataframe matches with the no.of. columns
                         available in the schema. If they are not matched
                         then further processing will be stopped
        Parameters
        ----------
        number_of_columns: int
                          length of the column present in
                           schema file
        input_data: pd.DataFrame
                 raw input dataframe

        Returns
        -------
            bool -> True (if invalid column length) , False( Valid column length)
        """
        if number_of_columns != input_data.shape[1]:
            return True
        else:
            return False

    def is_having_missing_values(self,
                                 input_data: pd.DataFrame
                                 ) -> tuple[bool, list]:
        """
            Description: This function validates if any column in the input
                         dataframe has all missing. In such case the
                         Dataframe will not be processed and will be skipped.

        Parameters
        ----------
        input_data: pd.DataFrame
                input dataframe
        Returns
        -------
         tuple[bool, list]

        """
        missing_values = False
        missing_columns = []
        for col in input_data.columns:
            if input_data[col].isnull().all():
                missing_values = True
                missing_columns.append(col)

        return missing_values, missing_columns

    def is_invalid_column_names(self,
                                column_details: dict,
                                input_data: pd.DataFrame
                                ) -> tuple[bool, list]:
        """
            Description: This method will verify if the given columns
                         are matching with the columns present in schema or not.

        Parameters
        ----------
        column_details: dict
                        Column name with data types
        input_data: input dataframe

        Returns
        -------
        tuple(bool,list)
                1) (True, [invalid column name list]) , for invalid column names
                2) (False, [] ), for valid column names
        """
        valid_column_names = column_details.keys()
        input_columns = input_data.columns

        invalid_column_names, invalid_col_list = False, []
        if sorted(valid_column_names) != sorted(input_columns):
            invalid_column_names = True
            invalid_col_list = set(input_columns) - set(valid_column_names)
            return invalid_column_names, invalid_col_list
        else:
            return invalid_column_names, invalid_col_list

    def convert_column_type(self,
                            input_data: pd.DataFrame,
                            obj_float_col: list):
        """
           Description:  convert the given list of columns to float

        Parameters
        ----------
        input_data: pd.DataFrame
                input dataframe

        obj_float_col: list of columns that should be converted to float
        Returns
        -------
        pd.DataFrame
        """
        try:
            for columns in obj_float_col:
                input_data[columns] = pd.to_numeric(input_data[columns], errors='coerce').astype(float)

            return input_data
        except Exception as e:
            self.logger.error(f" Error in converting OBJ column to FLOAT {e}")

    def is_invalid_data_type(self,
                             column_details: dict,
                             input_data: pd.DataFrame
                             ) -> tuple[bool, list]:
        """
            Description: This method will verify if the  data
                         types of columns are matching with
                         the schema or not.

        Parameters
        ----------
        column_details: dict
                      Column name with data types
        input_data: pd.DataFrame
                    input dataframe

        Returns
        -------
        tuple(bool,list)
                1) True, [invalid datatype column list]
                2) False, [],

        """
        invalid_dtypes = False
        invalid_dtypes_column = []
        input_data_dtypes = input_data.dtypes
        for column in list(input_data_dtypes.index):
            if input_data_dtypes[column] == float:
                if column_details[column] != "float":
                    invalid_dtypes = True
                    invalid_dtypes_column.append(column)
            elif input_data_dtypes[column] == object:
                if column_details[column] != "str":
                    invalid_dtypes = True
                    invalid_dtypes_column.append(column)

        return invalid_dtypes, invalid_dtypes_column
