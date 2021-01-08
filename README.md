# ServiceNow-UpdateDate-HDC
This is a Python project used to update ValidTo dates for articles that are out of date or soon to be out of date

## Environment
This project was built using:
- Python 3.8.6

Prepare Selenium
- Download `selenium-3.141.0.tar.gz`from repo
- Navigate to the file
- Unpack the file
- Install the module by executing `python3 setup.py install`

Prepare Firefox Driver
- Download `geckodriver` from repo
- Give executable permission `sudo chmod +x geckodriver`

## Execution
If Python3 is set as default:
`python SNow_Update_Date.py`

Otherwise:
`python3 SNow_Update_Date.py` 

During execution, the program relies on a CSV to read in articles in need of update. There are two methods that the CSV is loaded:
1. The CSV file can be preloaded as `kb_knowledge.csv` and will skip the auto-generated report process
2. If no file labeled as `kb_knowledge.csv` is found, the system will auto-generate a report with user input for filters  

Upon completion, all .csv and .log files will be removed as they are no longer needed.

<br />
<br />
<br />

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
