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

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)
driver.get("https://www.naukri.com/nlogin/login")

wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.getenv("NAUKRI_USER"))
wait.until(EC.presence_of_element_located((By.ID, "passwordField"))).send_keys(os.getenv("NAUKRI_PASS"))
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))).click()

time.sleep(5)
driver.get("https://www.naukri.com/mnjuser/profile")

# Trigger profile update by clicking Save
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))).click()

time.sleep(3) # wait a few seconds for the save to process before quitting
driver.quit()
