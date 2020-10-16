from selenium import webdriver
import time


details = {
    "Licence": "", # Full UK Licence
    "Booking_Ref": "", # Test Booking Refrence
    "Test_Center": "" # Name of Test Center
}

# Open Chrome

driver = webdriver.Chrome()

# Open the test management website and login
driver.get('https://driverpracticaltest.dvsa.gov.uk/login')
driver.find_element_by_id("driving-licence-number").send_keys(details["Licence"])
driver.find_element_by_id("application-reference-number").send_keys(details["Booking_Ref"])
driver.find_element_by_id("booking-login").click()

# Change test
driver.find_element_by_id("test-centre-change").click()
driver.find_element_by_id("test-centres-input").clear();
driver.find_element_by_id("test-centres-input").send_keys(details["Test_Center"])
driver.find_element_by_id("test-centres-submit").click()

# Select first test center
results_container = driver.find_element_by_class_name("test-centre-results")
test_center = results_container.find_element_by_xpath(".//a")
test_center.click()
