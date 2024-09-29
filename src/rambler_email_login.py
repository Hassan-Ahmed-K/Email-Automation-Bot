
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from src.custom_functions import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys



def wait_for_url_change(driver, target_url, timeout=30):
    try:
        # Wait until the current URL matches the target URL
        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url == target_url
        )
        print(f"URL changed to: {driver.current_url}")
        return True
    except Exception as e:
        print("Error or timeout while waiting for URL change:", e)
        return False


def ramble_login(driver,email,password):
    try:
        driver.maximize_window()

        driver.get("https://mail.rambler.ru/")

        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if driver.current_url.startswith("chrome-extension://"):
                driver.close()
        driver.switch_to.window(driver.window_handles[0])
        wait = WebDriverWait(driver=driver,timeout=30)
        try:
            time.sleep(5)
            iframe = driver.find_element(By.TAG_NAME,"iframe")
        except:
            time.sleep(60)
            iframe = driver.find_element(By.TAG_NAME,"iframe")

        driver.switch_to.frame(iframe)

        email_input = driver.find_element(By.ID, "login")
        type_like_human(email_input,email)

        password_input = driver.find_element(By.ID, "password")
        type_like_human(password_input,password)

        login_button = driver.find_element(By.CSS_SELECTOR, "button[data-cerber-id='login_form::main::login_button']")
        login_button.click()
        print("Login Button CLicked")
        try:
            h_captcha = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'iframe')))
            captcha_solver_status = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div.captcha-solver'))).text
            i=0
            print(captcha_solver_status != "Captcha solved!")
            while((captcha_solver_status != "Captcha solved!")):
                if(i==60):
                    break
                captcha_solver_status = driver.find_element(By.CSS_SELECTOR,'div.captcha-solver').text
                time.sleep(3)
                i+=1
            login_button = driver.find_element(By.CSS_SELECTOR, "button[data-cerber-id='login_form::main::login_button']")
            print(login_button.text)
            login_button.click()
            time.sleep(5)     
        except:
            print("Pass the H_Captcha")


        driver.refresh()
        time.sleep(5)

        try:
            target_url = "https://mail.rambler.ru/folder/INBOX"
            wait_for_url_change(driver, target_url)

            cross_button = WebDriverWait(driver=driver,timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button.styles-close-5S')))
            cross_button.click()
        except Exception as e:
            pass

        if (driver.current_url.startswith("https://mail.rambler.ru/folder/INBOX")):
            return True
        else:
            return False
    
    except Exception as e:
        print(e)
        return False
    

