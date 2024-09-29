from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import os
import random
# from src.rambler_email_login import ramble_login
# from src.rambler_send_email import rambler_send_email
import multiprocessing
import signal
import threading
from PIL import Image, ImageTk
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


stop_event = threading.Event()
# from docx import Document

def toggle_sender_email_input():
    """Toggle between showing the file path input or email text input based on checkbox selection."""
    if sender_email_from_file_var.get():
        sender_email_label.grid_remove()
        sender_email_input.grid_remove()
        sender_password_label.grid_remove()
        sender_password_input.grid_remove()
        sender_email_file_path_label.grid(row=1, column=0, pady=5, sticky="w")
        sender_email_file_path_input.grid(row=1, column=1, columnspan=2, pady=5)
        sender_email_browse_button.grid(row=1, column=3, padx=10, pady=5)
        
    else:
        sender_email_file_path_label.grid_remove()
        sender_email_file_path_input.grid_remove()
        sender_email_browse_button.grid_remove()
        sender_email_label.grid(row=1, column=0, pady=5, sticky="w")
        sender_email_input.grid(row=1, column=1, pady=5,sticky="w")
        sender_password_label.grid(row=2, column=0, pady=5, sticky="w")
        sender_password_input.grid(row=2, column=1, pady=5,sticky="w")

def toggle_email_subject_input():
    """Toggle between showing the file path input or email subject input based on checkbox selection."""
    if email_subject_from_file_var.get():
        # Show the file path inputs, hide the manual email subject input
        email_subject_label.grid_remove()
        email_subject_input.grid_remove()
        
        email_subject_file_path_label.grid(row=1, column=0, pady=5, sticky="w")
        email_subject_file_path_input.grid(row=1, column=1, pady=5, sticky="ew")
        email_subject_browse_button.grid(row=1, column=3, padx=5, pady=5)
    else:
        # Show the manual email subject input, hide the file path inputs
        email_subject_file_path_label.grid_remove()
        email_subject_file_path_input.grid_remove()
        email_subject_browse_button.grid_remove()
        
        email_subject_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        email_subject_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")

def toggle_recipient_email_input():
    """Toggle between showing the file path input or email text input based on checkbox selection."""
    if recipient_email_from_file_var.get():
        recipient_label.grid_remove()
        recipient_email_input.grid_remove()
        recipient_email_file_path_label.grid(row=4, column=0, pady=5, sticky="w")
        recipient_email_file_path_input.grid(row=4, column=1, columnspan=2, pady=5)
        recipient_email_browse_button.grid(row=4, column=3, padx=10, pady=5)
        # recipeint_email_browse_button.grid(row=2, column=2, padx=10, pady=5)
    else:
        recipient_email_file_path_label.grid_remove()
        recipient_email_file_path_input.grid_remove()
        recipient_email_browse_button.grid_remove()
        recipient_label.grid(row=4, column=0, pady=5, sticky="w")
        recipient_email_input.grid(row=4, column=1, pady=5,sticky="w")

def toggle_email_text_input():
    """Toggle between showing the file path input or email text input based on checkbox selection."""
    if email_text_from_file_var.get():
        email_text_input.grid_remove()
        email_text_file_path_input.grid_remove()
        email_text_file_path_label.grid(row=6, column=0, pady=5, sticky="w")
        email_text_file_path_input.grid(row=6, column=1, pady=5,sticky="w")
        browse_button.grid(row=6, column=2, padx=10, pady=5)
    else:
        email_text_file_path_input.grid_remove()
        email_text_file_path_label.grid_remove()
        browse_button.grid_remove()
        email_text_input_label.grid(row=6, column=0, pady=5, sticky="w")
        email_text_input.grid(row=6, column=1, columnspan=2, pady=5)

def browse_file(file_path_var):
    """Open a file dialog to select a file and update the file path input field."""
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)

def create_progress_popup():
    global progress_popup, progress_label, progress_bar

    # Create a new Toplevel window (popup)
    progress_popup = tk.Toplevel(root)
    progress_popup.title("Email Sending Progress")
    progress_popup.geometry("350x150")  # Adjust size as needed
    progress_popup.grab_set()  # Prevent interaction with main window

    # Setup the progress bar and label inside the popup
    progress_label = ttk.Label(progress_popup, text="Emails Sent: 0 / 0")
    progress_label.pack(pady=10)

    # Progress bar to show the percentage of completion
    progress_bar = ttk.Progressbar(progress_popup, orient="horizontal", mode="determinate", length=300)
    progress_bar.pack(pady=10)

    # Update the window to show changes
    progress_popup.update_idletasks()

def update_progress(sent, total):
    # Update the label and progress bar
    progress_label.config(text=f"Emails Sent: {sent} / {total}")
    progress_bar['value'] = (sent / total) * 100  # Set value as percentage
    progress_popup.update_idletasks()

def close_progress_popup():
    # Close the progress popup when done
    progress_popup.destroy()

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
            create_progress_popup()
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
                                # update_progress(recipient_number, total_recipients)
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

            close_progress_popup()
            messagebox.showinfo("Email Sending Complete", f"All {recipient_number} emails were successfully sent.")
  
            return True
        
        except:
            return False
        
def start_thread(asender_email, asender_password, arecipient_emails, aemail_subject, aemail_text, aemails_per_account, aproxy_flag):
    global email_thread  # Declare email_thread as global to access in stop_thread
    stop_event.clear()  # Clear the stop event
    email_thread = threading.Thread(target=rambler_send_email, args=(asender_email, asender_password, arecipient_emails, aemail_subject, aemail_text, aemails_per_account, aproxy_flag))
    email_thread.start()

def stop_thread():
    stop_event.set()  # Set the stop event to stop the thread
    if email_thread.is_alive():
        email_thread.join()  # Wait for the thread to finish if it's still alive
    print("Email sending has been stopped.")



if __name__ == '__main__':


    def get_values():
        sender_emails = ""
        sender_passwords = ""
        recipient_emails = ""
        email_texts = ""
        email_subjects = ""

        # Handling recipient emails
        if recipient_email_from_file_var.get():
            recipient_emails_path = recipient_email_file_path_var.get()
            if recipient_emails_path == "":
                messagebox.showerror("Input Error", "Please provide a valid file path for recipient emails.")
                return False, False, False, False
            try:
                recipient_emails = pd.read_csv(recipient_emails_path)["Email"].to_list()
                if not recipient_emails:
                    raise ValueError("Recipient email file is empty.")
            except Exception as e:
                messagebox.showerror("File Error", f"Error reading recipient email file: {e}")
                return False, False, False, False
        else:
            recipient_emails = recipient_email_input.get().split(",")
            if not recipient_emails or recipient_emails == [""]:
                messagebox.showerror("Input Error", "Please enter valid recipient emails.")
                return False, False, False, False

        # Handling email subject
        if email_subject_from_file_var.get():
            email_subject_path = email_subject_file_path_var.get()
            if email_subject_path == "":
                messagebox.showerror("Input Error", "Please provide a valid file path for email subject.")
                return False, False, False, False
            try:
                file_type = email_subject_path.split(".")[-1]
                if file_type == "txt":
                    with open(email_subject_path) as file:
                        email_subjects = [file.read()]
                elif file_type == "csv":
                    email_subjects = pd.read_csv(email_subject_path)["Email Subject"].to_list()
                else:
                    raise ValueError("Invalid file type for email subject.")
            except Exception as e:
                messagebox.showerror("File Error", f"Error reading email subject file: {e}")
                return False, False, False, False
        else:
            email_subjects = email_subject_input.get().split(",")
            if not email_subjects or email_subjects == [""]:
                messagebox.showerror("Input Error", "Please enter a valid email subject.")
                return False, False, False, False

        # Handling sender emails and passwords
        if not sender_email_from_file_var.get():
            sender_emails = sender_email_input.get().split(",")
            sender_passwords = sender_password_input.get().split(",")
            if not sender_emails or not sender_passwords or sender_emails == [""] or sender_passwords == [""]:
                messagebox.showerror("Input Error", "Please enter valid sender email(s) and password(s).")
                return False, False, False, False
        else:
            sender_emails_path = sender_email_file_path_var.get()
            if sender_emails_path == "":
                messagebox.showerror("Input Error", "Please provide a valid file path for sender emails.")
                return False, False, False, False
            try:
                df = pd.read_csv(sender_emails_path)
                sender_emails = df["Email"].to_list()
                sender_passwords = df["Email Password"].to_list()
                if not sender_emails or not sender_passwords:
                    raise ValueError("Sender email file is empty or missing necessary columns.")
            except Exception as e:
                messagebox.showerror("File Error", f"Error reading sender email file: {e}")
                return False, False, False, False

        # Handling email text
        if email_text_from_file_var.get():
            email_text_path = email_text_file_path_input.get()
            if email_text_path == "":
                messagebox.showerror("Input Error", "Please provide a valid file path for email text.")
                return False, False, False, False
            try:
                file_type = email_text_path.split(".")[-1]
                if file_type == "txt":
                    with open(email_text_path) as file:
                        email_texts = [file.read()]
                elif file_type == "csv":
                    email_texts = pd.read_csv(email_text_path)["Email Text"].to_list()
                else:
                    raise ValueError("Invalid file type for email text.")
            except Exception as e:
                messagebox.showerror("File Error", f"Error reading email text file: {e}")
                return False, False, False, False
        else:
            email_texts = [email_text_input.get("1.0", tk.END).strip()]
            if not email_texts or email_texts == [""]:
                messagebox.showerror("Input Error", "Please enter valid email text.")
                return False, False, False, False

        # Handling proxy flag and email per account
        proxy_flag = proxy_flag_var.get()
        print(f"Proxy is currently set to: {proxy_flag}")

        try:
            email_per_account = int(email_per_account_input.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for emails per account.")
            return False, False, False, False

        # Final check before starting the email sending process
        if not sender_emails or not sender_passwords or not recipient_emails or not email_subjects or not email_texts:
            messagebox.showerror("Missing Information", "All required information is not provided.")
            return False, False, False, False
        
        if(len(email_subjects) == 1):
            email_subjects = email_subjects * len(email_texts)
        
        if(len(email_subjects) != len(email_texts)):
            messagebox.showerror("Input Error", "Please enter Email Subjects Equals to Email Text.")
        
        print("Sender Email = ",len(sender_emails))
        print("Sender Password = ",len(sender_passwords))
        print("Recipient Email = ",len(recipient_emails))
        print("Email Subject = ",len(email_subjects))
        print("Email Text = ",len(email_texts))
        
        # Start the email sending process in a new thread
        start_thread(sender_emails, sender_passwords, recipient_emails, email_subjects, email_texts, email_per_account, proxy_flag)


    root = tk.Tk()
    root.title("Email Bot")
    root.configure(bg="#ffffff")

    icon_path = r"./assets/rambler.ico"
    img = Image.open(icon_path)
    tk_img = ImageTk.PhotoImage(img)

    root.wm_iconphoto(True, tk_img)

    header_bar = tk.Frame(root,bg="#F0F0F0")
    header_bar.pack(fill="x")

    icon_image = Image.open("./assets/rambler.ico")
    icon_image = icon_image.resize((40, 40))  # Resize the image if needed
    icon_image = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(header_bar, image=icon_image, bg="#f0f0f0")
    icon_label.pack(side="left",padx=10,pady=5)

    # Apply styling
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
    style.configure("TButton", background="#007BFF", foreground="#007BFF", font=("Arial", 12, "bold"))
    style.configure("TEntry", padding=(5, 2), foreground="black")
    style.configure("Header.TLabel", font=("Arial", 12, "bold"))
    style.configure("Info.TLabel", font=("Arial", 10, "bold"))
    style.configure("Custom.TCheckbutton", foreground="black", background="#f0f0f0", font=("Arial", 10, "bold"))
    style.configure("NameEntry.TEntry", padding=(5, 5), foreground="black", background="white")
    style.configure("Start.TButton", foreground="#4CAF50", background="#4CAF50", font=('Arial', 12, 'bold'))
    style.map("Start.TButton", background=[("active", "#4CAF50")])
    style.configure("Stop.TButton", foreground="#FF5722", background="#FF5722", font=('Arial', 12, 'bold'))
    style.map("Stop.TButton", background=[("active", "#FF5722")])
    style.configure("Tab.TFrame", background="#f0f0f0")
    style.configure("TRadiobutton", background="#f0f0f0", foreground="black", font=("Arial", 10))
    style.configure('TNotebook', background="#f0f0f0", borderwidth=2, relief="solid", height=0, width=0)


    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both')


    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Email Configuration")

    main_frame = ttk.Frame(tab1)
    main_frame.grid(row=0, column=0,padx=10)

    # ===========================================================================================================

    # Email Configuration Tab
    proxy_frame = ttk.Frame(main_frame, style='TFrame')
    proxy_frame.grid(row=0, column=0, sticky='w', padx=10)

    proxy_label = ttk.Label(proxy_frame, text="Select Proxy On or Off", style="TLabel")
    proxy_label.grid(row=0, column=0, padx=0, pady=5, sticky='w')

    proxy_flag_var = tk.StringVar(value="off")

    onn_radio = ttk.Radiobutton(proxy_frame, text="On", variable=proxy_flag_var, value="on", style="Custom.TRadiobutton")
    onn_radio.grid(row=1, column=0, sticky='w', padx=0, pady=5)

    off_radio = ttk.Radiobutton(proxy_frame, text="Off", variable=proxy_flag_var, value="off", style="Custom.TRadiobutton")
    off_radio.grid(row=1, column=1, sticky='w', padx=0, pady=5)


    # =========================================================================================

        # Email per Account Configuration
    email_per_account_frame = ttk.Frame(main_frame, style='TFrame')
    email_per_account_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    email_per_account_label = ttk.Label(email_per_account_frame, text="Email per Account:", style="TLabel")
    email_per_account_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    email_per_account_input = ttk.Entry(email_per_account_frame, style="TEntry")
    email_per_account_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

    email_per_account_frame.grid_columnconfigure(1, weight=1)

    # ===========================================================================================================


    # Create a new frame for the sender email configuration
    sender_frame = ttk.Frame(main_frame, style='TFrame')
    sender_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Sender email from file checkbox
    sender_email_from_file_var = tk.BooleanVar()
    sender_email_from_file_checkbox = ttk.Checkbutton(sender_frame, text="Use Sender Email From File", variable=sender_email_from_file_var, style="Custom.TCheckbutton", command=toggle_sender_email_input)
    sender_email_from_file_checkbox.grid(row=0, column=0, columnspan=3, pady=5, sticky="w")

    # Sender email file path label, entry, and browse button
    sender_email_file_path_var = tk.StringVar()
    sender_email_file_path_label = ttk.Label(sender_frame, text="Sender Email File Path:", style="TLabel")
    sender_email_file_path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    sender_email_file_path_input = ttk.Entry(sender_frame, textvariable=sender_email_file_path_var, style="TEntry")
    sender_email_file_path_input.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    sender_email_browse_button = ttk.Button(sender_frame, text="Browse", command=lambda: browse_file(sender_email_file_path_var), style="TButton")
    sender_email_browse_button.grid(row=1, column=2, padx=5, pady=5)

    # Sender email and password labels and entries
    sender_email_label = ttk.Label(sender_frame, text="Email:", style="TLabel")
    sender_email_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    sender_email_input = ttk.Entry(sender_frame, style="TEntry")
    sender_email_input.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

    sender_password_label = ttk.Label(sender_frame, text="Password:", style="TLabel")
    sender_password_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    sender_password_input = ttk.Entry(sender_frame, style="TEntry", show="*")
    sender_password_input.grid(row=3, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

    # Configure column weights for proper resizing
    sender_frame.grid_columnconfigure(1, weight=1)

    # Toggle input fields initially
    toggle_sender_email_input()

    # =========================================================================================

    # Create a new frame for the recipient email configuration
    recipient_frame = ttk.Frame(main_frame, style='TFrame')
    recipient_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Recipient email from file checkbox
    recipient_email_from_file_var = tk.BooleanVar()
    recipient_email_from_file_checkbox = ttk.Checkbutton(recipient_frame, text="Use Recipient Email Text from File", variable=recipient_email_from_file_var, style="Custom.TCheckbutton", command=toggle_recipient_email_input)
    recipient_email_from_file_checkbox.grid(row=0, column=0, columnspan=3, pady=5, sticky="w")

    # Recipient email file path label, entry, and browse button
    recipient_email_file_path_var = tk.StringVar()
    recipient_email_file_path_label = ttk.Label(recipient_frame, text="Recipient Email File Path:", style="TLabel")
    recipient_email_file_path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    recipient_email_file_path_input = ttk.Entry(recipient_frame, textvariable=recipient_email_file_path_var, style="TEntry")
    recipient_email_file_path_input.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    recipient_email_browse_button = ttk.Button(recipient_frame, text="Browse", command=lambda: browse_file(recipient_email_file_path_var), style="TButton")
    recipient_email_browse_button.grid(row=1, column=2, padx=5, pady=5)

    # Recipient email label and entry
    recipient_label = ttk.Label(recipient_frame, text="Recipient Email:", style="TLabel")
    recipient_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    recipient_email_input = ttk.Entry(recipient_frame, style="TEntry")
    recipient_email_input.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

    # Configure column weights for proper resizing
    recipient_frame.grid_columnconfigure(1, weight=1)

    # Toggle input fields initially
    toggle_recipient_email_input()


    # =========================================================================================

    # Email Subject Configuration

    email_subject_frame = ttk.Frame(main_frame, style='TFrame')
    email_subject_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Email Subject from file checkbox
    email_subject_from_file_var = tk.BooleanVar()
    email_subject_checkbox = ttk.Checkbutton(email_subject_frame, text="Use Email Subject from File", variable=email_subject_from_file_var, command=toggle_email_subject_input)
    email_subject_checkbox.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    # Email Subject file path label, entry, and browse button
    email_subject_file_path_var = tk.StringVar()
    email_subject_file_path_label = ttk.Label(email_subject_frame, text="Email Subject File Path:", style="TLabel")
    email_subject_file_path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    email_subject_file_path_input = ttk.Entry(email_subject_frame, textvariable=email_subject_file_path_var, style="TEntry")
    email_subject_file_path_input.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    email_subject_browse_button = ttk.Button(email_subject_frame, text="Browse", command=lambda: browse_file(email_subject_file_path_var), style="TButton")
    email_subject_browse_button.grid(row=1, column=2, padx=5, pady=5)

    # Email Subject label and entry
    email_subject_label = ttk.Label(email_subject_frame, text="Email Subject:", style="TLabel")
    email_subject_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    email_subject_input = ttk.Entry(email_subject_frame, style="TEntry")
    email_subject_input.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

    # Configure column weights for proper resizing
    email_subject_frame.grid_columnconfigure(1, weight=1)


    toggle_email_subject_input()

    # =============================================================================================

    # Create a new frame for the email text configuration
    email_text_frame = ttk.Frame(main_frame, style='TFrame')
    email_text_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Email text from file checkbox
    email_text_from_file_var = tk.BooleanVar()
    email_text_from_file_checkbox = ttk.Checkbutton(email_text_frame, text="Use Email Text from File", variable=email_text_from_file_var, style="Custom.TCheckbutton", command=toggle_email_text_input)
    email_text_from_file_checkbox.grid(row=0, columnspan=2, pady=5, sticky="w")

    # Email text file path label, entry, and browse button
    email_text_file_path_var = tk.StringVar()
    email_text_file_path_label = ttk.Label(email_text_frame, text="File Path:", style="TLabel")
    email_text_file_path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    email_text_file_path_input = ttk.Entry(email_text_frame, textvariable=email_text_file_path_var, style="TEntry",width=32)
    email_text_file_path_input.grid(row=1, column=1, pady=5, sticky="ew")

    browse_button = ttk.Button(email_text_frame, text="Browse", command=lambda: browse_file(email_text_file_path_var), style="TButton")
    browse_button.grid(row=1, column=2, padx=5, pady=5)

    # Email text input label and text area
    email_text_input_label = ttk.Label(email_text_frame, text="Email Text:", style="TLabel")
    email_text_input_label.grid(row=2, column=0, pady=5, sticky="ew")

    email_text_input = tk.Text(email_text_frame, height=5,width=40)
    email_text_input.grid(row=2, column=1, columnspan=2, pady=5, sticky="ew")

    # Configure column weights for proper resizing
    email_text_frame.grid_columnconfigure(1, weight=1)

    # Toggle input fields initially
    toggle_email_text_input()


    # Create a new frame for the buttons
    button_frame = ttk.Frame(main_frame, style='TFrame')
    button_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Start button
    start_button = ttk.Button(button_frame, text="Start", command=get_values, style="Start.TButton")
    start_button.grid(row=0, column=0, padx=5, pady=10)

    # Stop button
    stop_button = ttk.Button(button_frame, text="Stop", command=stop_thread, style="Stop.TButton")
    stop_button.grid(row=0, column=1, padx=5, pady=10)



    toggle_email_text_input()


    root.mainloop()
