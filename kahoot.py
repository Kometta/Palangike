import pathlib
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

default_download_path = pathlib.Path(__file__).parent.resolve().as_uri()

def fetch_kahoot_reports(username=None, password=None, download_dir=default_download_path):

    # Setup chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Do not show window
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    # Set Download path
    params = {'behavior': 'allow', 'downloadPath': download_dir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    # Open kahoot login page
    kahoot_login = 'https://create.kahoot.it/auth/login'
    driver.get(kahoot_login)

    # Login
    username_input = driver.find_element(By.CSS_SELECTOR, 'input#username')\
        .send_keys(username)

    password_input = driver.find_element(By.CSS_SELECTOR, 'input#password')\
        .send_keys(password)

    submit_button = driver.find_element(By.CSS_SELECTOR, 'button#login-submit-btn')\
        .click()

    sleep(1)
    driver.get('https://create.kahoot.it/user-reports')

    # Wait for page to load
    sleep(3)
    buttons = driver.find_elements(By.CSS_SELECTOR, 'tr[role="row"] button[data-functional-selector="report-action-menu__toggle"]')

    buttons[0].click()

    download_button = driver.find_element(By.CSS_SELECTOR, 'button#download')
    download_button.click()

    confirm_download_button = driver.find_element(By.CSS_SELECTOR, 'button[data-functional-selector="download-report-dialog__download-button"]')
    confirm_download_button.click()
    
    # Wait for download
    sleep(3)
