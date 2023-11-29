import pandas as pd
from housing_price.logger import logger
from housing_price.constants.common_constants import (
    COLUMN_FOR_ENCODING,
    ENCODED_COLUMNS
)
logger = logger.getChild(__name__)


class DataTransformation:
    """
        This class shall be used for transforming the valid raw data
        before loading it in Databse.

    """
    def __init__(self):
        self.logger = logger

    def drop_missing_values(
            self,
            input_data: pd.DataFrame
    ) -> pd.DataFrame:

        """
        Description: It will drop the rows having null

        Parameters
        ----------
        input_data : pd.DataFrame
            Input dataframe

        Returns
        -------
        pd.DataFrame
         DataFrame with dropped rows having null
        """
        record_length_before = input_data.shape[0]

        filtered_data = input_data.dropna()

        # There are some columns having "Null" present in string.
        # Those all should be dropped.

        for col in filtered_data.columns[filtered_data.dtypes == 'O']:
            filtered_data.drop(filtered_data[filtered_data[col]
                                             == 'Null'].index, inplace=True)

        record_length_after = filtered_data.shape[0]
        dropped_rows = record_length_before - record_length_after
        self.logger.info(f" Dropped {dropped_rows} rows from input dataframe")

        return filtered_data

    def add_missing_column_after_encoding(self,
                                          input_data: pd.DataFrame
                                          ) -> pd.DataFrame:
        """
            This method will add missing columns with 0 value.
            Example: In training data after encoding a column is converted
                    to 5 columns, But for prediction if it does not have 5 columns
                    then model will throw error.
        Parameters
        ----------
        input_data : pd.DataFrame
                Input dataframe

        Returns
        -------
        pd.DataFrame

        """

        missing_columns = set(ENCODED_COLUMNS) - set(input_data.columns)

        for columns in missing_columns:
            input_data[columns] = 0

        return input_data

    def perform_encoding(self,
                         input_data: pd.DataFrame,
                         columns_for_encoding: list) -> pd.DataFrame:
        """
            convert categorical columns to numerical form as ML models
            only accept numerical data.

        Parameters
        ----------
        input_data: pd.DataFrame
                 input datafrmae for encoding

        columns_for_encoding: List
                 list of columns for encoding

        Returns
        -------
        pd.Dataframe -> dataframe with encoded columns

        """
        input_data = pd.get_dummies(input_data, columns=columns_for_encoding)

        self.logger.info("Encoding done for categorical features")

        return input_data

