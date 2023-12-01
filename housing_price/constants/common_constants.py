
COL_NAME = 'col_name'

COLUMN_FOR_ENCODING = ['ocean_proximity']


COLUMNS_FOR_MODEL = ['longitude', 'latitude',
                     'housing_median_age',
                     'total_rooms', 'total_bedrooms',
                     'population', 'households',
                     'median_income', 'ocean_proximity_<1H OCEAN',
                     'ocean_proximity_INLAND', 'ocean_proximity_ISLAND',
                     'ocean_proximity_NEAR BAY', 'ocean_proximity_NEAR OCEAN']
ENCODED_COLUMNS = ['ocean_proximity_<1H OCEAN',
                   'ocean_proximity_INLAND',
                   'ocean_proximity_ISLAND',
                   'ocean_proximity_NEAR BAY',
                   'ocean_proximity_NEAR OCEAN']
NUMBER_OF_COLUMNS = 'number_of_columns'
OBJ_TO_FLOAT_COL = ['longitude', 
                    'latitude',
                    'housing_median_age',
                    'total_rooms',
                    'total_bedrooms',
                    'population',
                    'households',
                    'median_income',
                    ]
SCHEMA_FILE = "schema_prediction.json"
TRAINED_MODEL_PATH = "housing_price\\trained_model\\model.joblib"
TARGET_VARIABLE = "MEDIAN_HOUSE_PRICE"
VALID_OCEAN_PROXI_VALUES = ['NEAR OCEAN', 'INLAND', 'NEAR BAY', '<1H OCEAN',
                            'ISLAND', 'OUT OF REACH']


RENAMING_COL_FOR_DB = {
    'ocean_proximity_<1H OCEAN': 'ocean_proximity_LESS_H_OCEAN',
    'ocean_proximity_NEAR BAY': 'ocean_proximity_NEAR_BAY',
    'ocean_proximity_NEAR OCEAN': 'ocean_proximity_NEAR_OCEAN',
}
