from flask import Flask, request, jsonify
from flask import Response

import os
import pandas as pd

from validation_transformation import ValidationTransformation
from predict_from_model import Prediction
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

current_path = os.getcwd()


@app.route("/predict", methods=['POST'])
def predict_route():
    try:

        # Get input data from the request
        input_data = request.get_json()
        input_features = pd.DataFrame(input_data)
        print(input_features)

        # First perform validation and transformation of the data
        # Object initialization
        val_transform = ValidationTransformation(current_path)

        # calling the prediction_validation function
        transformed_data = val_transform.perform_validation_transformation(
            input_data)

        if not isinstance(transformed_data, pd.DataFrame):
            return jsonify({'prediction': "ERROR OCCURED"})

        pred = Prediction(current_path)  # object initialization

        # predicting for dataset present in databse

        predicted_data = pred.perform_prediction_from_model(transformed_data)

        print(predicted_data)
        return jsonify({'prediction': 10})

    except ValueError as ve:
        return Response(f"ERROR OCCURED. Got "
                        f"{ve.__class__.__name__} exception: {ve}")
    except KeyError as ke:
        return Response(f"ERROR OCCURED. Got "
                        f"{ke.__class__.__name__} exception: {ke}")
    except Exception as e:
        return Response(f"ERROR OCCURED. Got "
                        f"{e.__class__.__name__} exception: {e}")


port = int(os.getenv("PORT", 5001))
if __name__ == "__main__":
    app.run(port=port, debug=True)