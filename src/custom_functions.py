import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
import sys
import os
from dotenv import load_dotenv
import pyotp



def human_like_delay(min_delay=1, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))
    
def scroll(driver,scroll_value=500,down=True):
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.TAG_NAME, 'body'))
    if(down):
        actions.scroll_by_amount(0, scroll_value)
    else:
        actions.scroll_by_amount(scroll_value,0)
    actions.perform()
    human_like_delay()
    

def type_like_human(element, text, min_delay=0.0005, max_delay=0.0003):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))
        
        


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"stdout:\n{result.stdout}")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(f"stderr:\n{e.stderr}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")

def connect_protonvpn(server):
    command = [r'/usr/bin/protonvpn-cli', 'c', server]
    run_command(command)
    
# def connect_protonvpn(ser):
#     try:
#         # Construct the command to connect to ProtonVPN using the specified country code
#         command = ['protonvpn', '-', 'cli'," ","connect", country_code]
        
#         # Run the command
#         result = subprocess.run(command, capture_output=True, text=True)
        
#         # Check the result
#         if result.returncode == 0:
#             print(f"Connected to ProtonVPN server in country {country_code} successfully!")
#             print(result.stdout)
#         else:
#             print(f"Failed to connect to ProtonVPN server in country {country_code}.")
#             print(result.stderr)
#     except Exception as e:
#         print(f"An error occurred: {e}")

def disconnect_protonvpn():
    command = [r'/usr/bin/protonvpn-cli', 'd']
    run_command(command)


# def arkose_captcha_solver(site_key,url="https://x.com/account/access"):

#     load_dotenv()
#     api_key = os.getenv('APIKEY_2CAPTCHA')
#     print("API KEY = ",api_key)
#     solver = TwoCaptcha(api_key)
    
#     try:
#         result = solver.funcaptcha(sitekey=site_key,url=url)
#         captcha_token = result['code']
#         captcha_id = result['captchaId']
#         print(captcha_token)
#         return captcha_token
#     except Exception as e:
#         print("--------------------------")
#         print(e)
#         print("---------------------------------------")


def get_otp(secret_key):
    totp = pyotp.TOTP(secret_key)

    # Print current OTP
    print("Current OTP:", totp.now())
    
    return totp.now()
        
    # # Wait for the OTP to expire
    # time.sleep(30)

    # # Print new OTP
    # print("New OTP:", totp.now())
    
    


def get_proxy_from_file(proxy_file_path):
    try:
        with open(proxy_file_path, 'r') as file:
            proxies = file.readlines()
        selected_proxy = random.choice(proxies).strip().split(":")[:2]

        return ":".join(selected_proxy)
    except (FileNotFoundError, IndexError):
        return None
