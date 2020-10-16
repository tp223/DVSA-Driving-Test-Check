from selenium import webdriver
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# Ensure that your details are copied into launchDVSA.py to
# quickly login when tests become available

details = {
    "Licence": "", # Full UK Driving Licence
    "Booking_Ref": "", # Current Test Booking Refrence
    "Test_Center": "" # Test Center Name / Postcode
}

smtp = {
    "sender": "test-availability@example.com", # SMTP sender address
    "sender_title": "DVSA Test Check", # SMTP sender name
    "recipient": "recipient@example.com", # Notification recipient
    "server": "smtp.example.com", # SMTP server address
    "login": "server-admin@example.com", # SMTP server login
    "password": "password" # SMTP server password
}

# Use Chrome for website
driver = webdriver.Chrome()

# Open the test booking management website
driver.get('https://driverpracticaltest.dvsa.gov.uk/login')

# Login with current test details
driver.find_element_by_id("driving-licence-number").send_keys(details["Licence"])
driver.find_element_by_id("application-reference-number").send_keys(details["Booking_Ref"])
driver.find_element_by_id("booking-login").click()

# Change test center option
driver.find_element_by_id("test-centre-change").click()
driver.find_element_by_id("test-centres-input").clear();
driver.find_element_by_id("test-centres-input").send_keys(details["Test_Center"])
driver.find_element_by_id("test-centres-submit").click()

# Select first test center
results_container = driver.find_element_by_class_name("test-centre-results")
test_center = results_container.find_element_by_xpath(".//a")
test_center.click()

#Check if any tests avaliable
if "There are no tests available" in driver.find_element_by_id("main").get_attribute('innerHTML'):
    driver.quit()
    print("No test available")
else:
    print("Tests available, sending email...")

    message = """
    Driving test has become available at """ + details["Test_Center"] + """.
    https://driverpracticaltest.dvsa.gov.uk/manage
    """

    # Create message
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] =  Header("Cancellation Available", 'utf-8')
    msg['From'] = formataddr((str(Header(smtp["sender_title"], 'utf-8')), smtp["sender"]))
    msg['To'] = smtp["recipient"]

    # Create server object with SSL option
    server = smtplib.SMTP_SSL(smtp["server"], 465)

    # Perform operations via server
    server.login(smtp["login"], smtp["password"])
    server.sendmail(sender, [smtp["recipient"]], msg.as_string())
    server.quit()
    
    print("Sent!")

    driver.quit()
