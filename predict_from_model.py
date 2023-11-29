import pandas as pd

from housing_price.constants.common_constants import (
    TRAINED_MODEL_PATH,
    TARGET_VARIABLE,
)
from housing_price.constants.db_constants import (
    DB_NAME,
    PREDICTED_DATA_TABLE_NAME,
)
from housing_price.database.db_operations import DataBaseOperation
from housing_price.logger import logger
import joblib
logger = logger.getChild(__name__)


class Prediction:
    """
        class to perform load the model and perform prediction

    """
    def __init__(self, current_path):
        self.path = current_path
        self.logger = logger
        self.db_operations = DataBaseOperation(current_path)

    def load_model(self):
        """
            Description: Load the trained model for prediction

        Returns
        -------
        joblib file
        """
        try:
            with open(TRAINED_MODEL_PATH, 'rb') as file:
                loaded_model = joblib.load(file)
            self.logger.info(" Model loaded successfully.")

        except FileNotFoundError:
            self.logger.error(f"Error: File not found. Please check the "
                              f"file path: {TRAINED_MODEL_PATH}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")

        return loaded_model

    def perform_prediction(self,
                           model,
                           input_features: pd.DataFrame
                           ) -> pd.DataFrame:
        """
            Description: This method will do prediction and
                         return the predicted values
        Parameters
        ----------
        model:
            loaded model

        input_features: pd.DataFrame
                    transformed data for prediction

        Returns
        -------
        pd.DataFrame
            dataframe with predicted values

        """
        try:
            output_variable = model.predict(input_features)
            input_features[TARGET_VARIABLE] = output_variable

            return input_features

        except Exception as e:
            self.logger.error(f" Error in prediction : {e} ")

    def perform_prediction_from_model(self,
                                      input_features: pd.DataFrame
                                      ) -> pd.DataFrame:
        """
            Description: This method will load the model. predict the
                         target variable and save the prediction in
                         the database
        Parameters
        ----------
        input_features: independent features to pass to model
                        for prediction.

        Returns
        -------
        pd.DataFrame
            dataframe with dependent and independent variables.
        """

        try:
            # Load the model
            model = self.load_model()

            # perform prediction
            predicted_data = self.perform_prediction(model, input_features)

            self.logger.info(" Prediction done successfully")
            # save the prediction in database
            self.logger.info(" Creating the Prediction table")
            self.db_operations.create_db_table(
                DB_NAME,
                PREDICTED_DATA_TABLE_NAME
            )
            self.logger.info(" Loading the data to Prediction table")
            self.db_operations.insert_into_table(
                DB_NAME,
                predicted_data,
                PREDICTED_DATA_TABLE_NAME
            )
            return predicted_data
        except Exception as e:
            self.logger.error(f" Error in prediction : {e} ")

