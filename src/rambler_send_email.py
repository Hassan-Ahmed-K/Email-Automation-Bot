from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.custom_functions import *
from selenium.webdriver.common.keys import Keys
from src.rambler_email_login import ramble_login
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import math
import tkinter as tk
from tkinter import ttk
import time


def get_proxy_from_file(proxy_file_path):
    try:
        with open(proxy_file_path, 'r') as file:
            proxies = file.readlines()
        selected_proxy = random.choice(proxies).strip().split(":")[:2]
        return ":".join(selected_proxy)
    except (FileNotFoundError, IndexError):
        return None

def create_progress_bar():
    global root,progress_label, progress_bar, status_frame
    # Setup the GUI
    # Frame for status and progress bar
    status_frame = ttk.Frame(root, padding="10")
    status_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # Progress label to show the status of email sending
    progress_label = ttk.Label(status_frame, text="Emails Sent: 0 / 0")
    progress_label.grid(row=0, column=0, padx=10, pady=10)

    # Progress bar to show the percentage of completion
    progress_bar = ttk.Progressbar(status_frame, orient="horizontal", mode="determinate", length=300)
    progress_bar.grid(row=1, column=0, padx=10, pady=10)

    root.update_idletasks()


def update_progress(sent, total):
    progress_label.config(text=f"Emails Sent: {sent} / {total}")
    progress_bar['value'] = sent
    root.update_idletasks()

def rambler_send_email(asender_email,asender_password,recipient_emails,email_subjects,email_texts,emails_per_account,proxy_flag):     
        try:
            current_working_directory = os.getcwd()
            captcha2_extension_path = os.path.join(current_working_directory, "Extentions/captcha2_extention")

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(f"--load-extension={captcha2_extension_path}")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            prefs = {
                "profile.default_content_setting_values.notifications": 2  # 1: Allow, 2: Block
            }
            chrome_options.add_experimental_option("prefs", prefs)

            
            recipient_number = 0
            email_text_no = 0
            total_recipients =  len(recipient_emails)
            create_progress_bar()
            update_progress(recipient_number, total_recipients)

            print(len(recipient_emails))
            
            while(recipient_number < len(recipient_emails)):
                driver = None
                login_status = False
                
                while not(login_status):
                    print("Login Loop")
                    proxy_file_path = './assets/proxies.txt'

                    proxy = get_proxy_from_file(proxy_file_path)

                    if(proxy_flag == "on"):
                        print("Proxy = ",proxy)
                        chrome_options.add_argument(f'--proxy-server={proxy}')

                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    driver.maximize_window()

                    index = random.randint(0, len(asender_email))

                    sender_email = asender_email[index]
                    sender_password = asender_password[index]

                    print("=================================================")
                    print("sender_email = ",sender_email)
                    print("sender_password = ",sender_password)
                    print("==================================================")

                    # Login to Rambler
                    login_status = ramble_login(driver=driver, email=sender_email, password=sender_password)

                    
                    if (not login_status):
                        print(f"Login failed for {sender_email}, retrying...")
                        driver.quit()

                print("login Status = ",login_status)
                if (login_status):
                    wait = WebDriverWait(driver, 10)
                    j=0
                    print("emails_per_account = ",emails_per_account)
                    for j in range(emails_per_account):
                        print("=================================================")
                        print("j= ",j)
                        print("recipient_number =",recipient_number)
                        try:
                            recipient_email = recipient_emails[recipient_number]
                            print("recipient_email = ",recipient_email)
                            email_text = email_texts[email_text_no]
                            print("email_text = ",email_text)
                            email_subject = email_subjects[email_text_no]
                            print("email_subject = ",email_subject)
                            if(recipient_email !="" or recipient_email != None):
                                print("recipient_number=",recipient_number)
                                print("recipient_email=", recipient_email)
                                try:
                                    header_continer = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.Header-headLinks-1F")))
                                    write_btn = header_continer.find_element(By.CSS_SELECTOR,'button[type="button"]')

                                    write_btn.click()
                                    time.sleep(5)
                                except:
                                    print("Write Button Not Found")
                                
                                eamil_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#composeScrollableArea")))

                                email_reciver_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#receivers")))
                                # for recipient_email in recipient_emails:
                                type_like_human(email_reciver_input,recipient_email)
                                # email_reciver_input.send_keys(recipient_email)
                                email_reciver_input.send_keys(Keys.RETURN)
                                email_topic_input = eamil_container.find_element(By.CSS_SELECTOR,"input#subject")
                                type_like_human(email_topic_input,email_subject)
                                email_textbox = driver.find_element(By.TAG_NAME, "iframe")
                                driver.switch_to.frame(email_textbox)

                                email_body = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div')))
                                email_body.click()
                                type_like_human(email_body,email_text)
                                # email_body.send_keys(email_text)

                                driver.switch_to.default_content()
                                main_container = driver.find_element(By.CSS_SELECTOR,"div.ComposeGrid-popupwindow-1k")
                                footer = main_container.find_element(By.CSS_SELECTOR,"div.Compose-send-2l")
                                
                                send_btn = footer.find_element(By.CSS_SELECTOR, "button")
                                send_btn.click()

                                print("Email sent to: ",recipient_email)
                                time.sleep(17)
                                recipient_number += 1
                                email_text_no +=1

                            else:
                                recipient_number+=1
                            
                            update_progress(recipient_number, total_recipients)

                            if(recipient_number >= len(recipient_emails)):
                                break

                            if(email_text_no >= len(email_texts)):
                                email_text_no=0
                        except Exception as e:
                            print(e)
                print("Driver = ",driver)
                if (driver):
                    driver.quit()
            
  
            return True
        
        except:
            return False
        
        
        


