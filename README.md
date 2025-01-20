
# **Email Automation Bot using Rambler Accounts**

## **Project Description:**

The **Email Automation Bot** is a Python-based solution designed to streamline and automate the process of sending emails through Rambler accounts. The bot is equipped with a user-friendly **Tkinter GUI** that allows users to manage the email-sending process with multiple options, including manual input and CSV file uploads for account credentials, recipient emails, email subjects, and message content. It also features **proxy support** for secure email sending and includes a progress tracker for real-time updates.

---

## **Key Features:**

1. **Proxy Support:**
   - The bot includes a radio button option to enable or disable proxy usage for email sending, allowing users to ensure anonymity or bypass IP restrictions.

2. **Email Sending Limits:**
   - Users can specify the **number of emails to send per Rambler account**. Once the limit is reached, the bot automatically switches to the next available account.

3. **Account Credentials Input:**
   - Users have the option to:
     - **Manually enter** Rambler email and password for sending emails.
     - **Browse and upload a CSV file** containing multiple Rambler account credentials. The bot will randomly select and rotate through accounts based on the user-defined email-sending limit.

4. **Recipient Email Input:**
   - Users can:
     - **Manually input multiple recipient emails**, separating them with commas.
     - **Upload a CSV file** containing recipient email addresses for batch emailing.

5. **Email Subject Input:**
   - Users can:
     - **Manually input the subject** of the email.
     - **Browse and upload a CSV or TXT file** containing multiple email subjects.

6. **Email Body Input:**
   - Users can:
     - **Manually input the email text** in a text area.
     - **Upload a CSV or TXT file** with pre-defined email messages.
     - Multiple email texts can only be read from a CSV file, allowing the bot to send unique messages per recipient.

7. **Email Sending Process:**
   - The bot logs into each Rambler account and sends emails to the recipients, switching accounts once the user-defined limit is reached.
   - The process continues until emails are sent to all recipients provided by the user.

8. **Progress Tracking:**
   - The bot features a **progress pop-up window** with a progress bar, allowing users to track the email-sending process in real time.

9. **Start and Stop Buttons:**
   - Users can control the bot with **Start** and **Stop** buttons in the GUI. Once the bot is started, it runs based on the input parameters provided by the user.

---

## **Workflow:**
1. **Login**: The bot logs into the Rambler email account.
2. **Email Sending**: It sends the defined number of emails (per account) as specified by the user.
3. **Switch Accounts**: Once the email limit is reached, the bot switches to the next Rambler account.
4. **Continue**: The bot continues this process until all recipient emails have been sent.

---

## **Technology Stack:**
- **Python**: Core programming language.
- **Tkinter**: Used for building the GUI.
- **Selenium**: For automating the web-based login and email-sending process.
- **CSV File Handling**: To manage multiple Rambler accounts, recipient lists, email subjects, and message texts.
- **Proxy Support**: Integrated to enable anonymous or secure email sending through different IP addresses.

---

## **Usage:**
1. **Input your Rambler accounts** (manually or via CSV file).
2. **Set the email sending limit per account**.
3. **Provide recipient email addresses** (manually or via CSV file).
4. **Input the email subject** (manually or via file upload).
5. **Write the email text** (manually or via CSV/TXT file).
6. **Start the bot** and track progress through the progress bar.

This bot simplifies bulk emailing by automating account management, email sending, and message personalization.
