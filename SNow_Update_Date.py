import time
import csv
import os
import sys
import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
import selenium.webdriver.common.action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


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
'''  # TODO

## ---------------------------------------------------------------------------- ##


def find_elem_by_xpath(xpath):
    var_name = ''
    attempt_count = 0

    while(True):
        try:
            var_name = driver.find_element(By.XPATH, xpath)
        except Exception:
            if attempt_count < 20:
                pass
            else:
                print("Unexpected error:", sys.exc_info()[0])
                driver.quit()
                raise

        if not isinstance(var_name, str):
            return var_name

        attempt_count += 1
        time.sleep(0.5)


## ---------------------------------------------------------------------------- ##


def find_elem_by_css(selector):
    var_name = ''
    attempt_count = 0

    while(True):
        try:
            var_name = driver.find_element(By.CSS_SELECTOR, selector)
        except Exception:
            if attempt_count < 20:
                pass
            else:
                print("Unexpected error:", sys.exc_info()[0])
                driver.quit()
                raise

        if not isinstance(var_name, str):
            return var_name

        attempt_count += 1
        time.sleep(0.5)


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


def servicenow_select_table():
    # Pick which table to pull from
    find_elem_by_xpath('//*[@id="select2-chosen-1"]').click()

    # Enter search info
    find_elem_by_xpath(
        '//*[@id="s2id_autogen1_search"]').send_keys('Knowledge [kb_knowledge]')

    # Select 'Knowledge [kb_knowledge]'
    kb_button = ''

    find_elem_by_xpath('//span[text()="Knowledge [kb_knowledge]"]').click()


## ---------------------------------------------------------------------------- ##


def servicenow_fill_report_form():
    # Switch to the correct frame
    driver.switch_to.frame('gsft_main')

    # Find report name and set as 'KCS Knowledge Base'
    find_elem_by_xpath(
        '//*[@id="report-name"]').send_keys('KCS Knowledge Base')

    # Check to see Source Type is Table
    # print(driver.find_element(By.XPATH, '//*[@id="select-source-type"]').get_property('label'))

    # Select proper table
    servicenow_select_table()

    # Click the next button to load results
    find_elem_by_xpath('//*[@id="next-button-step-1"]').click()


## ---------------------------------------------------------------------------- ##


def servicenow_filter_results():
    # Click filter results
    find_elem_by_xpath('//*[@id="open-filters-button"]').click()


## ---------------------------------------------------------------------------- ##


def servicenow_create_report():
    # Go to Create Report page
    driver.get(
        'https://tamuplay.service-now.com/nav_to.do?uri=%2Fsys_report_template.do%3Fsysparm_create%3Dtrue')

    servicenow_fill_report_form()
    servicenow_filter_results()

    # wait till kb_knowledge.csv has downloaded
    kb_file = os.path.join(cwd, 'kb_knowledge.csv')

    print('1. Add desired filters.')
    print('2. Press \'Run\'.)
    print('3. Right-Click Numbers > Export > CSV > Download')

    while not os.path.exists(kb_file):
        time.sleep(2.5)

## ---------------------------------------------------------------------------- ##
# TODO Navigate to Reports and generate CSV


def generate_kb_list():
    servicenow_create_report()

    print('\n Generating KB_Kist...')
    temp_kb_list = csv_read('kb_knowledge.csv')

    for article in temp_kb_list:
        if article == number:
            continue
        else:
            kb_list.append(article)

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
    find_elem_by_xpath('//*[@data-mce-src="/tamu_stack.png"]').click()


## ---------------------------------------------------------------------------- ##


def enter_user():
    # Input desired username here
    driver.find_element(By.ID, 'username').send_keys('txconnorriley')

    # Selects the password field so user can begin typing
    driver.find_element(By.ID, 'password').click()


## ---------------------------------------------------------------------------- ##


def job_start():
    print('\nBeginning Valid To Update')
    print('There are ' + str(number_of_articles), end='')
    print(' articles that need to updated.')


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
    # job_start()


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
# Update method to rely on correct page,
# not waiting a set period of time


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

    job_complete()


## ---------------------------------------------------------------------------- ##
# Open the website tamuplay
driver.get('https://tamuplay.service-now.com/')

# Login to tamuplay
servicenow_login()

# For all KBs in the list, process valid_to dates
# Search > Edit > Checkout > Update > Publish
servicenow_process_kbs()

driver.quit()
