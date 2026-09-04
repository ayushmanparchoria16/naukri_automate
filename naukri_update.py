from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://www.naukri.com/nlogin/login")

driver.find_element(By.ID, "usernameField").send_keys(os.getenv("NAUKRI_USER"))
driver.find_element(By.ID, "passwordField").send_keys(os.getenv("NAUKRI_PASS"))
driver.find_element(By.XPATH, "//button[text()='Login']").click()

time.sleep(5)
driver.get("https://www.naukri.com/mnjuser/profile")

# Trigger profile update by clicking Save
driver.find_element(By.XPATH, "//button[text()='Save']").click()

driver.quit()
