import time
import csv
import os
import sys
import datetime
from datetime import date

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# Using Firefox to access web
driver = webdriver.Firefox(executable_path=os.path.abspath('geckodriver'))
count = 0
number_of_articles = 0
start_time = 0

'''  # TODO
- Automate pulling KCS Knowledge Base entries
- Download as CSV to working directory
- Parse CSV using existing function csv_read
'''  # TODO


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
    cwd = os.getcwd()
    f = os.listdir(cwd)

    # Instantiate list for csv files
    csv_f = []

    # Check list of all files for all csv files
    # Add csv files ot list of csv files
    for x in f:
        if x.endswith('.csv'):
            csv_f.append(x)

    kb_list = []

    # For all csv files read in report
    for csv_file in csv_f:
        print('Now reading \"' + csv_file + '\"...')
        temp_kb_list = csv_read(csv_file)

        for article in temp_kb_list:
            kb_list.append(article)

        print('...Finished reading \"' + csv_file + '\"!')

    print('...KB_List generated!')
    return kb_list


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


def job_complete():
    print(' ')
    print('******************')
    print('** JOB COMPLETE **')
    print('******************')
    print(' ')

    time.sleep(10)


def select_tamu_login():
    tamu_login = driver.find_element(
        By.XPATH, "//*[@data-mce-src='/tamu_stack.png']")
    tamu_login.click()


def enter_user():
    # Input desired username here
    driver.find_element(By.ID, 'username').send_keys('txconnorriley')

    # Selects the password field so user can begin typing
    driver.find_element(By.ID, 'password').click()


def servicenow_login():
    # Automate some of the login process
    print('\nLogging in')

    select_tamu_login()
    enter_user()


def interact_search_field(search_field, kb_number):
    print('Searching for: ' + kb_number)

    search_field.clear()
    search_field.send_keys(kb_number)
    search_field.send_keys(Keys.RETURN)

    time.sleep(0.5)


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


# This method needs to be updated to edit only ValidTo dates, no longer a need to pull Meta Tags
def servicenow_update_valid_to(kb_number):
    # Find edit button and click
    meta_tag_field = ''
    scrape_count = 0

    while(True):
        try:
            meta_tag_field = driver.find_element(By.ID, 'kb_knowledge.meta')
        except Exception:
            pass

        if not isinstance(meta_tag_field, str):
            print('Scraping Meta Tags: ' + kb_number)
            meta_tags = meta_tag_field.get_attribute('value')
            tag_list.append([kb_number, meta_tags])
            break

        if scrape_count == 10:
            servicenow_edit_kb(kb_number)
            return

        scrape_count += 1

        time.sleep(0.5)


def servicenow_process_kb(kb_number):
    servicenow_search(kb_number)
    time.sleep(1)


def job_start():
    print('\nBeginning Meta Tag Scrape')
    print('There are ' + str(number_of_articles), end='')
    print(' articles that need to be scraped.')


def print_progress():
    percent_done = round(float(count) / float(number_of_articles) * 100.0, 2)
    print('\n----- ' + str(percent_done) + '% -----')
    print('Time elapsed: %s s \n' % round(time.time() - start_time, 2))


# Open the website tamuplay
driver.get('https://tamuplay.service-now.com/')

# Login to tamuplay
servicenow_login()

# Wait for user to finish logging in
while 'tamuplay' not in driver.current_url:
    time.sleep(1)

# Start the clock
start_time = time.time()
job_start()

# TODO Navigate to Reports and generate CSV
kb_list = generate_kb_list()
number_of_articles = len(kb_list)

# For all KBs in the list, process valid_to dates
for article in kb_list:
    servicenow_process_kb(article)
    print_progress()
    count += 1

job_complete()
driver.quit()
