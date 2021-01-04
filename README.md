# ServiceNow-UpdateDate-HDC
This is a Python project used to update ValidTo dates for articles that are out of date or soon to be out of date

## Environment
This project was built using:
- Python 3.8.6

Prepare Selenium
- Download *selenium-3.141.0.tar.gz*
- Navigate to the file
- Unpack the file
- Install the module by executing `python3 setup.py install`

Prepare Firefox Driver
- Download geckodriver from Repo

Prepare CSV file
- Go to tamu.service-now.com
- Run report with Table "Knowledge [kb_knowledge]"
- Set filters to "Knowledge Base is KCS" and "Workflow is Published"
- Click "Run"
- Right-click the header row
- Click "Export" > "CSV"
- Download the exported CSV file to the directory of the Repo

## Execution
If Python3 is set as default:
`python SNow_Update_Date.py`

Otherwise:
`python3 SNow_Update_Date.py`
<br />
<br />
<br />
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
