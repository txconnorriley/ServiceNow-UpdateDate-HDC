import time
import csv
import os
import sys
import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

## ---------------------------------------------------------------------------- ##
# Establishing user profile for Firefox

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.getcwd())
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

# Using Firefox to access web
driver = webdriver.Firefox(
    profile, executable_path=os.path.abspath('geckodriver'))

## ---------------------------------------------------------------------------- ##
# Establishing global variables

count = 0
number_of_articles = 0
start_time = 0
cwd = os.getcwd()

## ---------------------------------------------------------------------------- ##

'''  # TODO
- Automate pulling KCS Knowledge Base entries
- Download as CSV to working directory
- Parse CSV using existing function csv_read
- Readd updating Valid To dates
'''  # TODO

## ---------------------------------------------------------------------------- ##


def print_progress():
    percent_done = round(float(count) / float(number_of_articles) * 100.0, 2)
    print('\n----- ' + str(percent_done) + '% -----')
    print('Time elapsed: %s s \n' % round(time.time() - start_time, 2))


## ---------------------------------------------------------------------------- ##


def calc_valid_to_date():
    # Editing current date to Valid_To date
    today = date.today()
    valid_to_date = today.replace(year=(today.year + 1))
    return valid_to_date.strftime("%Y-%m-%d")


## ---------------------------------------------------------------------------- ##

def calc_current_date():
    today = date.today()
    return today.strftime("%m/%d/%Y")


## ---------------------------------------------------------------------------- ##


def str_to_date(date_str):
    # Passed in using mm/dd/yyyy format
    # Date wants yyyy-mm-dd
    temp_list = date_str.split('/')
    return date(int(temp_list[2]), int(temp_list[0]), int(temp_list[1]))


## ---------------------------------------------------------------------------- ##
# TODO Navigate to Reports and generate CSV


def generate_kb_list():
    ''' 
    # Navigating to Reports page
    # Switch to the correct frame
    driver.switch_to.default_content()

    # Check to make sure that the Navigator pane is open (is 'Minimize Navigator')
    title="Minimize Navigator"

    # Select Filter Navigator
    id="filter"

    # Send keys "Reports"
    text = "Reports"

    # Change click Create New
    text = "Create New"

    # Switch back to the main frame
    driver.switch_to.frame('gsft_main')

    # Fill out report name
    id="report-name"
    send key "KCS Knowledge Base"

    # Check to see Source Type is Table
    id="select-source-type"

    # Pick which table to pull from
    id="select2-chosen-1"
    send key "Knowledge [kb_knowledge]"

    # Click the next button to load results
    id="next-button-step-1"

    # Click filter results
    id="open-filters-button"

    # Select Field button
    text="-- choose field --"
    send key "Knowledge base"
    send key "DOWN"
    send key "ENTER"

    # Select KCS
    id="select2-drop-mask"
    send key "KCS"
    send key "ENTER"

    # Add an AND condition
    data-original-title="Add AND condition"

    # Select Field button
    text="-- choose field --"
    send key "Workflow"
    send key "DOWN"
    send key "ENTER"

    # Select Published
    label="-- None --"
    label="Published"

    # Add an AND condition
    data-original-title="Add AND condition"

    # Select Field button
    text="-- choose field --"
    send key "Valid to"
    send key "DOWN"
    send key "ENTER"

    # Select Before
    label="on"
    label="before"

    # Select Today
    text="-- None --"
    text="Days"
    text="Today"

    # Run Report
    id="run-report"

    # Export CSV
    text = "Number"
    *RIGHT CLICK*
    text = "Export"
    text = "CSV"

    # Select Download
    id="download_button"

    '''

    print('Generating KB_Kist...')
    files = os.listdir(cwd)

    # Instantiate list for csv files
    csv_files = []

    # Check list of all files for all csv files
    # Add csv files ot list of csv files
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(file)

    kb_list = []

    # For all csv files read in report
    for csv_file in csv_files:
        print('Now reading \"' + csv_file + '\"...')
        temp_kb_list = csv_read(csv_file)

        for article in temp_kb_list:
            kb_list.append(article)

        print('Finished reading \"' + csv_file + '\"!')

    print('KB_List generated!')
    return kb_list


## ---------------------------------------------------------------------------- ##


def csv_read(csv_name):
    # kb[0], valid_to[1]
    with open(csv_name, 'rt', encoding='ISO-8859-1') as current:
        reader = csv.reader(current, delimiter=',')

        kb_list = []

        # Read CSV file row by row
        for row in reader:
            # Search queries are found in the second column
            kb_article = row[0]
            kb_list.append(kb_article)

        return kb_list


## ---------------------------------------------------------------------------- ##


def select_tamu_login():
    tamu_login = driver.find_element(
        By.XPATH, "//*[@data-mce-src='/tamu_stack.png']")
    tamu_login.click()


## ---------------------------------------------------------------------------- ##


def enter_user():
    # Input desired username here
    driver.find_element(By.ID, 'username').send_keys('txconnorriley')

    # Selects the password field so user can begin typing
    driver.find_element(By.ID, 'password').click()


## ---------------------------------------------------------------------------- ##


def job_start():
    print('\nBeginning Meta Tag Scrape')
    print('There are ' + str(number_of_articles), end='')
    print(' articles that need to be scraped.')


## ---------------------------------------------------------------------------- ##


def servicenow_login():
    # Automate some of the login process
    print('\nLogging in')

    select_tamu_login()
    enter_user()

    # Wait for user to finish logging in
    while 'tamuplay' not in driver.current_url:
        time.sleep(1)

    # Start the clock
    start_time = time.time()
    job_start()


## ---------------------------------------------------------------------------- ##


def remove_csv_files():
    print('Removing .csv files...')

    # Get current working directory and files within

    files = os.listdir(cwd)

    # Instantiate list for csv files
    csv_files = []

    # Check list of all files for all csv files
    # Add csv files ot list of csv files
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(file)

    # If there are no csv files, exit
    if len(csv_files) == 0:
        print('No .csv files found...\n')
        return

    # If there are csv files, remove them
    for file in csv_files:
        # Join file to cwd to get abs path
        file_to_remove = os.path.join(cwd, file)

        # Remove file
        print('Removing ' + file + '...')
        os.remove(file_to_remove)


## ---------------------------------------------------------------------------- ##


def remove_log_files():
    print('Removing .log files...')

    # Get current working directory and files within
    files = os.listdir(cwd)

    # Instantiate list for log files
    log_files = []

    # Check list of all files for all log files
    # Add log files ot list of log files
    for file in files:
        if file.endswith('.log'):
            log_files.append(file)

    # If there are no log files, exit
    if len(log_files) == 0:
        print('No .log files found...\n')
        return

    # If there are log files, remove them
    for file in log_files:
        # Join file to cwd to get abs path
        file_to_remove = os.path.join(cwd, file)

        # Remove file
        print('Removing ' + file + '...')
        os.remove(file_to_remove)


## ---------------------------------------------------------------------------- ##


def job_complete():
    print(' ')

    # Clean up cwd after execution
    remove_csv_files()
    remove_log_files()

    print(' ')
    print('******************')
    print('** JOB COMPLETE **')
    print('******************')
    print(' ')

    time.sleep(10)


## ---------------------------------------------------------------------------- ##


def interact_search_field(search_field, kb_number):
    print('Searching for: ' + kb_number)

    search_field.clear()
    search_field.send_keys(kb_number)
    search_field.send_keys(Keys.RETURN)

    time.sleep(0.5)


## ---------------------------------------------------------------------------- ##


def servicenow_search(kb_number):
    driver.switch_to.default_content()

    # Type in search field and search for article
    search_field = ''
    search_count = 0

    while(True):
        try:
            search_field = driver.find_element(By.ID, 'sysparm_search')
        except Exception:
            pass

        if not isinstance(search_field, str):
            interact_search_field(search_field, kb_number)
            break

        if search_count == 10:
            return

        search_count += 1

        time.sleep(0.5)

    servicenow_edit_kb(kb_number)


## ---------------------------------------------------------------------------- ##


def servicenow_edit_kb(kb_number):
    # Change the frame
    driver.switch_to.frame('gsft_main')

    # Find edit button and click
    edit_button = ''
    edit_count = 0

    while(True):
        try:
            edit_button = driver.find_element(
                By.XPATH, "//*[@id='editArticle']")
        except Exception:
            pass

        if not isinstance(edit_button, str):
            print('Editing article: ' + kb_number)
            edit_button.click()
            break

        if edit_count == 10:
            return

        edit_count += 1

        time.sleep(0.5)

    servicenow_update_valid_to(kb_number)


## ---------------------------------------------------------------------------- ##
# Update method to rely on correct page,
# not waiting a set period of time


def servicenow_checkout_kb(kb_number):
    time.sleep(0.5)
    checkout_button = ''
    count = 0

    while(True):
        try:
            checkout_button = driver.find_element(
                By.XPATH, "//button[@name='not_important']")
        except Exception:
            pass

        if not isinstance(checkout_button, str):
            print('Checking out article: ' + kb_number)
            checkout_button.click()
            time.sleep(2)
            break

        if count >= 5:
            servicenow_edit_kb(kb_number)

        count += 1

        time.sleep(2)


## ---------------------------------------------------------------------------- ##
# Update method to rely on correct page,
# not waiting a set period of time


def servicenow_update_valid_to(kb_number):
    valid_to_field = ''
    count = 0
    while(True):
        try:
            valid_to_field = driver.find_element(
                By.ID, 'kb_knowledge.valid_to')
        except Exception:
            pass

        if not isinstance(valid_to_field, str):
            print('Updating from: ' + valid_to_field.get_attribute('value'))

            # Clear current value, and update to one year from current date
            valid_to_field.clear()
            valid_to_field.send_keys(calc_valid_to_date())
            print('Updating to: ' + calc_valid_to_date())
            break

        if count == 6:
            driver.switch_to.default_content()
            servicenow_edit_kb(kb_number)

        count += 1
        time.sleep(2)


## ---------------------------------------------------------------------------- ##


def servicenow_publish_kb(kb_number):
    publish_button = ''
    while(True):
        try:
            publish_button = driver.find_element(
                By.XPATH, "//button[@id='publish_knowledge']")
        except Exception:
            pass

        if not isinstance(publish_button, str):
            print('Publishing article: ' + kb_number)
            publish_button.click()
            break

        time.sleep(2)


## ---------------------------------------------------------------------------- ##


def servicenow_process_kbs():
    # Generate KB list and update global num_articles
    kb_list = generate_kb_list()
    number_of_articles = len(kb_list)

    # For each article in the list...
    for article in kb_list:
        # Begin the process by searching
        servicenow_search(article)

        # Print the progress and increment by one
        print_progress()
        count += 1

        # Give time for the system to recover
        time.sleep(1)


## ---------------------------------------------------------------------------- ##
# Open the website tamuplay
driver.get('https://tamuplay.service-now.com/')

# Login to tamuplay
servicenow_login()

# For all KBs in the list, process valid_to dates
# Search > Edit > Checkout > Update > Publish
servicenow_process_kbs()

job_complete()
driver.quit()
