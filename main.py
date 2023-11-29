import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TRAIN_DATA = 'housing_price/training_data/housing.csv'
MODEL_NAME = 'housing_price/trained_model/model.joblib'
RANDOM_STATE=100

def prepare_data(input_data_path):
    df=pd.read_csv(input_data_path)
    df=df.dropna()

    for col in df.columns[df.dtypes == 'O']:  # 'Null' is present in the categorical columns also.
        df.drop(df[df[col] == 'Null'].index, inplace=True)

    # encode the categorical variables
#    df = pd.get_dummies(df)


    df_features= df.drop(['MEDIAN_HOUSE_VALUE', 'AGENCY'], axis=1)
    y=df['MEDIAN_HOUSE_VALUE'].values

    # encoding OCEAN_PROXIMITY
    df_features = pd.get_dummies(df_features, columns=['OCEAN_PROXIMITY'])

    # filtering only required columns for model
    filtered_columns = ['LONGITUDE', 'LAT', 'MEDIAN_AGE', 'ROOMS', 'BEDROOMS', 'POP',
                        'HOUSEHOLDS', 'MEDIAN_INCOME', 'OCEAN_PROXIMITY_<1H OCEAN',
                        'OCEAN_PROXIMITY_INLAND', 'OCEAN_PROXIMITY_ISLAND',
                        'OCEAN_PROXIMITY_NEAR BAY', 'OCEAN_PROXIMITY_NEAR OCEAN']
    df_features = df_features.loc[:,filtered_columns]

    # renameing column : If not done..it will just thorw warning message.
    column_mapping = {'LONGITUDE': 'longitude',
                      'LAT': 'latitude',
                      'MEDIAN_AGE': 'housing_median_age',
                      'ROOMS': 'total_rooms',
                      'BEDROOMS': 'total_bedrooms',
                      'POP': 'population',
                      'HOUSEHOLDS': 'households',
                      'MEDIAN_INCOME': 'median_income',
                      'OCEAN_PROXIMITY_<1H OCEAN': 'ocean_proximity_<1H OCEAN',
                      'OCEAN_PROXIMITY_INLAND': 'ocean_proximity_INLAND',
                      'OCEAN_PROXIMITY_ISLAND': 'ocean_proximity_ISLAND',
                      'OCEAN_PROXIMITY_NEAR BAY': 'ocean_proximity_NEAR BAY',
                      'OCEAN_PROXIMITY_NEAR OCEAN': 'ocean_proximity_NEAR OCEAN'
                      }
    df_features.rename(columns=column_mapping, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(df_features, y, test_size=0.2, random_state=RANDOM_STATE)

    return (X_train, X_test, y_train, y_test)

def train(X_train, y_train):
    # what columns are expected by the model
    X_train.columns

    regr = RandomForestRegressor(max_depth=12)
    regr.fit(X_train,y_train)

    return regr

def predict(X, model):
    Y = model.predict(X)
    return Y

def save_model(model, filename):
    with open(filename, 'wb'):
        joblib.dump(model, filename, compress=3)

def load_model(filename):
    model = joblib.load(filename)
    return model

if __name__ == '__main__':
    logging.info('Preparing the data...')
    X_train, X_test, y_train, y_test = prepare_data(TRAIN_DATA)

    # the model was already trained before
    # logging.info('Training the model...')
    # regr = train(TRAIN_DATA)

    # the model was already saved before into file 'model.joblib'
    # logging.info('Exporting the model...')
    # save_model(regr, MODEL_NAME)

    logging.info('Loading the model...')
    model = load_model(MODEL_NAME)

    logging.info('Calculating train dataset predictions...')
    y_pred_train = predict(X_train, model)
    logging.info('Calculating test dataset predictions...')
    y_pred_test = predict(X_test, model)

    # evaluate model
    logging.info('Evaluating the model...')
    train_error = mean_absolute_error(y_train, y_pred_train)
    test_error = mean_absolute_error(y_test, y_pred_test)

    logging.info('First 5 predictions:')
    logging.info(f'\n{X_test.head()}')
    logging.info(y_pred_test[:5])
    logging.info(f'Train error: {train_error}')
    logging.info(f'Test error: {test_error}')
