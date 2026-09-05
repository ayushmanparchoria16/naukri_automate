from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

if not os.getenv("NAUKRI_USER") or not os.getenv("NAUKRI_PASS"):
    raise ValueError("NAUKRI_USER or NAUKRI_PASS environment variables are missing or empty. Please check your GitHub Secrets!")

try:
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for the login form to load and interact with it carefully (for React state)
    username_el = wait.until(EC.element_to_be_clickable((By.ID, "usernameField")))
    username_el.click()
    username_el.clear()
    username_el.send_keys(os.getenv("NAUKRI_USER"))
    time.sleep(1)
    
    password_el = wait.until(EC.element_to_be_clickable((By.ID, "passwordField")))
    password_el.click()
    password_el.clear()
    password_el.send_keys(os.getenv("NAUKRI_PASS"))
    time.sleep(1)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))).click()
    
    time.sleep(5)
    # Take a screenshot to see what Naukri shows after clicking login (e.g. OTP prompt, invalid password, or success)
    driver.save_screenshot("after_login.png")
    
    driver.get("https://www.naukri.com/mnjuser/profile")
    
    # Trigger profile update by clicking Save
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))).click()
    
    time.sleep(3) # wait a few seconds for the save to process before quitting

except Exception as e:
    print(f"Error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
    raise e

finally:
    driver.quit()
