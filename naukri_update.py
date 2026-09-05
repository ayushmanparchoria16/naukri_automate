import os, time
import imaplib
import email
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_latest_otp(email_user, email_pass):
    print("Waiting for OTP email to arrive (15 seconds)...")
    time.sleep(15)
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")
        
        # Search for unread emails from info@naukri.com
        status, messages = mail.search(None, '(UNSEEN FROM "info@naukri.com")')
        if status != 'OK' or not messages[0]:
            print("No unread email found from Naukri.")
            return None
            
        # Get the latest email
        latest_email_id = messages[0].split()[-1]
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        elif part.get_content_type() == "text/html":
                            body += part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                    
                # Extract 6-digit OTP
                match = re.search(r'\b\d{6}\b', body)
                if match:
                    return match.group(0)
    except Exception as e:
        print(f"Failed to fetch OTP: {e}")
    finally:
        try:
            mail.logout()
        except:
            pass
    return None

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
    
    # Check if OTP prompt appeared
    verify_buttons = driver.find_elements(By.XPATH, "//button[text()='Verify']")
    if len(verify_buttons) > 0:
        print("OTP prompt detected! Attempting to read email...")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
        if not gmail_pass:
            raise ValueError("GMAIL_APP_PASSWORD is not set in secrets! Cannot fetch OTP.")
            
        otp = get_latest_otp(os.getenv("NAUKRI_USER"), gmail_pass)
        if otp:
            print("Successfully retrieved OTP from email.")
            otp_boxes = driver.find_elements(By.XPATH, "//input[@type='text' or @type='number' or @type='tel']")
            visible_boxes = [box for box in otp_boxes if box.is_displayed()]
            
            if len(visible_boxes) >= 6:
                for i in range(6):
                    visible_boxes[i].send_keys(otp[i])
            elif len(visible_boxes) > 0:
                visible_boxes[0].send_keys(otp)
                
            time.sleep(1)
            verify_buttons[0].click()
            time.sleep(5)
        else:
            raise Exception("Could not find OTP in email or email did not arrive.")

    driver.save_screenshot("after_login.png")
    
    driver.get("https://www.naukri.com/mnjuser/profile")
    
    # Trigger profile update by clicking Save
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))).click()
    
    time.sleep(3)
    print("Profile successfully updated!")

except Exception as e:
    print(f"Error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
    raise e

finally:
    driver.quit()
