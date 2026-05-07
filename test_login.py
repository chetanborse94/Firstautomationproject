from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Disable headless mode for debugging
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the login page
try:
    print("Opening website...")
    driver.get('https://driver007.com/admin/')
    print("Website opened successfully!")
    
    # Take a screenshot to see what's on the page
    driver.save_screenshot('page_screenshot.png')
    print("Screenshot saved as 'page_screenshot.png'")
    
    # Wait for page to fully load
    sleep(3)
    
    # Try to find all input fields on the page
    all_inputs = driver.find_elements(By.TAG_NAME, 'input')
    print(f"Found {len(all_inputs)} input fields on the page")
    for i, inp in enumerate(all_inputs):
        field_id = inp.get_attribute('id')
        field_name = inp.get_attribute('name')
        field_type = inp.get_attribute('type')
        print(f"  Input {i}: id='{field_id}', name='{field_name}', type='{field_type}'")
    
except Exception as e:
    print(f"Error opening website: {e}")
    driver.quit()
    exit()

try:
    # Find the username and password input fields and enter the credentials
    print("\nAttempting login...")
    print("Finding email field...")
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'validation-form-2')))
    print("Entering email...")
    email_input.send_keys('sst.superadmin@yopmail.com')

    print("Finding password field...")
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'validation-form-3')))
    print("Entering password...")
    password_input.send_keys('admin@321')

    # Submit the login form
    print("Submitting login form...")
    password_input.send_keys(Keys.RETURN)

    # Wait for the page to load after login
    print("Waiting for login to complete...")
    sleep(5)
    print("Login form submitted successfully!")
except Exception as e:
    print(f"Error during login: {e}")
finally:
    # Close the browser
    driver.quit()