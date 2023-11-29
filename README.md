# DTSE Data Engineer (ETL) assignment

## Project Overview

Brief description of your data science project.

## Prerequisites

List the prerequisites needed to run your project. Include information about the required software, packages, and any other dependencies.

* Python 3.9.13
* pip 
* Virtual environment (optional but recommended)


## Installation 
(These steps are for Windows machine.)

1) Clone the repository to your local machine:
    git clone https://github.com/
2) Navigate to the project directory:               
    ``` cd housing_price```                       
3) Create a virtual environment (optional but recommended):                     
   ```python -m venv venv```                         
   or                                    
   Manually create from IDE.
4) Activate the virtual environment.                                    
    * on windows                            
      ```venv\Scripts\activate```               
5) Install project dependencies:                           
  ``` pip install -r requirements.txt ```


##---------------------
## Usage

Once the installation is done run the below command to start the API.

   ```python app.py```

Open your web browser and go to http://localhost:5001/predict to access the app.


Note: Port number may change sometime. So please pass the port number shown after the ```python app.py.```




######################################




This app.py program takes input in the form of json.

### Project Structure

Describe the structure of your project, including key directories and files.
```
housing_price/                           
│      
├── housing_price/                       
│   ├── constants                  
│   ├── databse           
│   ├── pipeline           
│   ├── trained_model         
│   ├── training_data                       
├── tests/                                        
├── app.py                                      
├── predict_from_model.py                                              
├── requirements.txt                                        
├── schema_prediction.json                                         
├── setup.py                    
├── template.py      
└── validation_transformation.py                                     
```

### Files
* `app.py` - Flask program which will open the endpoint. User will pass input data to this end point.
* `predict_from_model.py` -  This program will load the model, perform prediction and save the data in DB.  
* `model.joblib` - the computed model you should use 
* `housing.csv` - data file to process and apply a model to it for creating predictions
* `requirements.txt` - pip dependencies
* `schema_prediction.json` - schema of input data.
* `validation_transformation.py` - This Script will perform validation and transformation of input data


## Getting Started



## Mandatory Task
1. Create a functionality in python (understand as script or multiple scripts, classes, functions, etc.) that processes input (`housing.csv`), transforms it, saves it to db, provides it to a model and saves the predictions in db again. Usually data is provided to us in nonstandardized format by customer and we need to be sure it's processed correctly for our model to be able to generate predictions.
2. Demonstrate with a provided test data that it works and how it should be used (`housing.csv`)
3. After installing new libraries, update requirements.txt file
4. Create a new readme file describing new functionality and how to use the processing pipeline for preparation of input for data modeling

## Optional Tasks and topics for discussion
1. Logging - how and why would you implement it?
2. Tests - how and why would you implement it?
3. Exception handling - how and why would you implement it?
4. API - how and why would you implement it?

## Submitting your solution
The preferred form of submission is to place the whole solution in a public GitHub repository and send us a link. Both the dataset and model are distributed under the public license. If you don't wish to display your solution publicly, you can add repository view permissions to the email kosztolanyistefan@gmail.com or send a zip archive with the code to the same email address.

## Notes
* You should not generate any new model. Use the model provided in the `model.joblib` file.
* If you use a database, is should be part of your solution as a file.
* If something is unclear or you run into any technical diffilcuties, feel free to contact us.
* Python 3.9.13 was tested with the solution, thus this version is recommended to use. Use a different version at your own risk.

### Files
* `main.py` - sample script that generates and uses the model for predictions
* `model.joblib` - the computed model you should use 
* `housing.csv` - data file to process and apply a model to it for creating predictions
* `requirements.txt` - pip dependencies

## Sample outputs
You can validate you predictions on these sample inputs and expected outputs.

Input 1:
```
longitude: -122.64
latitude: 38.01
housing_median_age: 36.0
total_rooms: 1336.0
total_bedrooms: 258.0
population: 678.0
households: 249.0
median_income: 5.5789
ocean_proximity: 'NEAR OCEAN'
```

Output 1: `320201.58554044`

-----------------------------------

Input 2:
```
longitude: -115.73
latitude: 33.35
housing_median_age: 23.0
total_rooms: 1586.0
total_bedrooms: 448.0
population: 338.0
households: 182.0
median_income: 1.2132
ocean_proximity: 'INLAND'
```
Output 2: `58815.45033765`

-----------------------------------

Input 3:
```
longitude: -117.96
latitude: 33.89
housing_median_age: 24.0
total_rooms: 1332.0
total_bedrooms: 252.0
population: 625.0
households: 230.0
median_income: 4.4375
ocean_proximity: '<1H OCEAN'
```
Output 3: `192575.77355635`
