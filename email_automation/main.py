import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import os

# --- File Paths ---
SOURCE_CSV = "/Users/akishress/Desktop/MST/data"
LOG_CSV = "/Users/akishress/Desktop/MST/data_sent"

# Point to your panda image here
IMAGE_PATH = "/Users/akishress/Desktop/MST/panda.png"

# --- Zoho Credentials ---
ZOHO_USER = ""
ZOHO_PASSWORD = ""  # Use your Zoho App Password here

def send_personalized_html_emails():
    # Connect to Zoho SMTP
    server = smtplib.SMTP("smtp.zoho.com", 587)
    server.starttls()
    server.login(ZOHO_USER, ZOHO_PASSWORD)

    # Email subject
    subject = "Collaboration Opportunity – We Want You!"

    # Updated HTML email template with placeholders for {name} and the flex-based footer layout.
    # The panda image is wrapped in an anchor tag so that clicking it goes to the shortcut URL.
    html_template = """\
<html>
<body>
  <p>Hi, {name}!</p>

  <p>
    Thank you for registering with 
    <a href="https://shorturl.at/btZWw">Kung Fu Quiz (KFQ)</a> 
    – the ultimate online quiz-making tool!
    We’re excited to welcome you to our growing community of educators, 
    dedicated to making learning interactive and impactful for students.
  </p>

  <p>
    As a new quiz-making platform with a mission to transform the teaching game, 
    we are seeking to collaborate with passionate and like-minded teachers like you 
    to help us spread the word.
  </p>

  <p>
    With Kung Fu Quiz, you can easily transform your YouTube video lessons 
    into engaging quiz games and assessment resources. 
    This makes lesson planning quicker, boosts student engagement, 
    and offers a valuable teaching resource.
  </p>

  <p>
    To show you how students can participate in the Kung Fu Quiz,
    we’ve prepared a demo quiz for you to try. 
    Simply enter your name and join the quiz.
    <br/>
    👉🏼 <a href="https://kungfuquiz.net/?code=ADB382">https://kungfuquiz.net/?code=ADB382</a>
  </p>

  <p>
    Your input is invaluable, and we’d love to explore the possibilities of working together.<br>
    Interested? Simply reach out to us for more information.
    Looking forward to hearing from you <strong>:)</strong>
  </p>

  <p>
    With Regards,<br>
    [Your Name/Team]
  </p>

  <hr>
  <footer style="font-family: Arial, sans-serif; color: #000;">
    <div style="display: flex; align-items: center; margin-top: 10px;">
      <!-- Left: Panda Logo (bigger size) wrapped in a clickable link -->
      <a href="https://shorturl.at/btZWw" target="_blank">
        <img src="cid:footer_image" alt="Kung Fu Quiz Logo" style="width: 120px; margin-right: 10px;" />
      </a>

      <!-- Right: Text Content -->
      <div>
        <div style="font-size: 18px; font-weight: bold;">Kung Fu Quiz</div>
        <div style="margin-bottom: 4px;">Marketing Team</div>
        <!-- Red line full width -->
        <hr style="border: 1px solid #D10000; width: 100%; margin: 8px 0;">
        <div>marketing@kungfuquiz.com</div>
        <!-- Clickable website -->
        <div>
          <a href="https://www.kungfuquiz.com" style="text-decoration: none; color: inherit;">www.kungfuquiz.com</a>
        </div>
      </div>
    </div>
  </footer>
</body>
</html>
"""

    # Prepare the log file (data_sent)
    file_exists = os.path.isfile(LOG_CSV)
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as logfile:
        writer = csv.writer(logfile)
        
        # If "data_sent" doesn't exist yet, create a header
        if not file_exists:
            writer.writerow(["name", "email", "status", "date"])

        # Read the source CSV
        with open(SOURCE_CSV, "r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            
            # Skip the header if present
            header = next(reader, None)
            
            for row in reader:
                # Handle rows with 2 or 3 columns (to manage possible extra commas)
                if len(row) == 2:
                    name, email = row
                elif len(row) == 3:
                    name, _, email = row
                else:
                    # Skip malformed rows
                    continue

                # Clean up whitespace
                name = name.strip()
                email = email.strip()

                if not email:
                    # Log entries without a valid email
                    writer.writerow([name, "", "No Email", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    continue

                # Create a MIMEMultipart message with "related" type for inline image support
                msg = MIMEMultipart("related")
                msg["Subject"] = subject
                msg["From"] = ZOHO_USER
                msg["To"] = email

                # Create an alternative part for the HTML content
                msg_alternative = MIMEMultipart("alternative")
                msg.attach(msg_alternative)

                # Format the HTML with the personalized name
                html_body = html_template.format(name=name)
                msg_alternative.attach(MIMEText(html_body, "html"))

                # Attach the image as an inline attachment
                try:
                    with open(IMAGE_PATH, "rb") as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header("Content-ID", "<footer_image>")
                        img.add_header("Content-Disposition", "inline", filename=os.path.basename(IMAGE_PATH))
                        msg.attach(img)
                except Exception as img_error:
                    print(f"Failed to attach image for {name} <{email}>. Error: {img_error}")
                    writer.writerow([name, email, "Failed to attach image", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    continue

                # Send the email
                status = "Success"
                try:
                    server.send_message(msg)
                    print(f"Sent to {name} <{email}>")
                except Exception as e:
                    print(f"Failed to send to {name} <{email}>. Error: {e}")
                    status = "Failed"

                # Log the email sending attempt
                writer.writerow([
                    name,
                    email,
                    status,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])

    # Close the SMTP connection
    server.quit()

if __name__ == "__main__":
    send_personalized_html_emails()
