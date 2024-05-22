from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_webdriver_instance():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # Optional, for headless mode
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def enter_phone_number_otp(driver, phone_number, otp):
    driver.find_element_by_xpath("//input[@class = 'phone-number']").send_keys(phone_number)
    driver.find_element_by_id("send-otp-btn-id").click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    otp_fields = driver.find_elements_by_xpath("//input[@class = 'otp-digit-input']")
    for field, digit in zip(otp_fields, otp):
        field.send_keys(digit)
    driver.find_element_by_id("submit-otp-btn-id").click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))

def login(driver):
    driver.get("https://accounts.teachmint.com/")
    enter_phone_number_otp(driver, "8827415689", "264734")

def main():
    driver = get_webdriver_instance()
    login(driver)

def navigate_to_certificates(driver):
    certificates_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Certificates')]") #Unable to find xpath for certificate as we should be able to have the certificate page available live to us
    certificates_link.click()
    WebDriverWait(driver, 30).until(EC.url_contains("certificates"))
    time.sleep(2)

# Function to select the certificate type
def select_certificate_type(driver):
    certificate_type_dropdown = driver.find_element(By.ID, "certificate-type-dropdown")
    certificate_type_dropdown.click()
    time.sleep(1)
    certificate_option = driver.find_element(By.XPATH, "//div[@role='option' and contains(text(), 'School Leaving Certificate')]") #Unable to find xpath for certificate as we should be able to have the certificate page available live to us
    certificate_option.click()
    time.sleep(1)

# Function to search and select a student
def search_and_select_student(driver, student_name):
    search_box = driver.find_element(By.ID, "search-input")
    search_box.send_keys(student_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    first_result = driver.find_element(By.XPATH, "//div[@class='search-result-item']") #Unable to find xpath for search as we should be able to have the page available live to us
    first_result.click()
    time.sleep(1)

# Function to click the generate button
def click_generate(driver):
    generate_button = driver.find_element(By.ID, "generate-btn") #Unable to find xpath for generate button as we should be able to have the page available live to us
    generate_button.click()
    time.sleep(2)

# Function to update remarks
def update_remarks(driver, remarks_text):
    remarks_input = driver.find_element(By.ID, "remarks-textarea") #Unable to find xpath for remarks as we should be able to have the page available live to us
    remarks_input.clear()
    remarks_input.send_keys(remarks_text)
    time.sleep(1)

# Function to generate and download the certificate
def generate_and_download(driver):
    generate_download_button = driver.find_element(By.ID, "generate-download-btn") #Unable to find xpath for generate-download button as we should be able to have the page available live to us
    generate_download_button.click()
    time.sleep(2)

# Function to validate the certificate history
def validate_certificate_history(driver):
    history_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Certificate History')]") #Unable to find xpath for history-link as we should be able to have the page available live to us
    history_link.click()
    WebDriverWait(driver, 30).until(EC.url_contains("certificate-history"))
    time.sleep(2)

# Function to automate generating a certificate for Sam
def automate_generate_certificate_for_sam(driver, student_name='Sam', remarks_text='Generated for Sam'):
    navigate_to_certificates(driver)
    select_certificate_type(driver)
    search_and_select_student(driver, student_name)
    click_generate(driver)
    update_remarks(driver, remarks_text)
    generate_and_download(driver)
    validate_certificate_history(driver)

# Main function to run the automation
def main():
    driver = get_webdriver_instance()
    login(driver)
    automate_generate_certificate_for_sam(driver)
    driver.quit()

if __name__ == "__main__":
    main()