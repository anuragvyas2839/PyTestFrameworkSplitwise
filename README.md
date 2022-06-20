# PyTestFrameworkSplitwise
A Pytest Framework designed to test Splitwise api using mocks.

## Requirements
Python 3.  
The libraries to be installed prior to running the tests are mentioned [here](https://github.com/anuragvyas2839/PyTestFrameworkSplitwise/blob/main/requirements.txt).

## How to run?
Clone the project : [URL](https://github.com/anuragvyas2839/PyTestFrameworkSplitwise.git).    
In your terminal, navigate inside the project directory PyTestFrameworkSplitwise.    
Run all cases with command : pytest.   
It will run all the tests inside the project and generate a report.    
If you want to run a particular group of tests like smoke, regression, acceptance, use -m flag, eg :      
- pytest -m smoke : It will run all the cases marked as smoke.      
- pytest -m "smoke and regression" : It will run all the cases marked as smoke as well as regression.
- pytest -m "smoke or regression" : It will run all the cases marked as either smoke or regression.
- pytest -m "not smoke" : It will run all the cases which are not marked as smoke.

## Check report
Upon running the tests, report will get generated along with timestamp inside the **reports** directory.    
A sample report has been generated and already present inside the **reports** directory. 
