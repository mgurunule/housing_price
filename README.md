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
    git clone https://github.com/mgurunule/housing_price.git
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


## Usage

1) Once the installation is done run the below command to start the API.

   ```python app.py```

2) run test_app.py from thr project.

Note: Please verify the api url of ```test_app.py``` with the url genarated by running ```app.py``` Port number 
      may change sometime. So please pass the port number shown after the ```python app.py```.                    
      If not same please modify the url in ```test_app.py```


3) test_app.py will print the expected dataframe with predicted value.


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
* `test_app.py` - script to test the execution of api

## Getting Started


