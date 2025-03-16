# email_automation
# Email Automation

This project is an automated email sender that uses Zoho's SMTP server to send personalized HTML emails. It reads contact information from a CSV file, sends customized emails with an embedded clickable panda logo in the footer, and logs the status of each email sent.

## Features

- **Personalized Emails:**  
  Each email is customized with the recipient's name.
  
- **HTML Email Template:**  
  Emails include formatted HTML content with a clickable inline image (panda logo) in the footer.
  
- **CSV Integration:**  
  Reads contacts from a source CSV file and logs email sending status (success/failure) in a separate CSV file.
  
- **SMTP via Zoho:**  
  Uses Zoho's SMTP server for sending emails securely.

## File Structure

- **email_automation.py:**  
  The main Python script that sends the emails.

- **Source CSV (`data`):**  
  The CSV file containing contact details. Expected to have either 2 columns (name, email) or 3 columns (name, extra field, email).

- **Log CSV (`data_sent`):**  
  The file where email sending attempts are logged.

- **Panda Logo (`panda.png`):**  
  The image file used in the email footer. This image is clickable and redirects users to a specified URL.

## Prerequisites

- Python 3.x  
- Standard Python libraries (csv, smtplib, email, datetime, os) are used.  
- A Zoho account with SMTP access (use your Zoho App Password).

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone git@github.com:akiShresss/email_automation.git
   cd email_automation
