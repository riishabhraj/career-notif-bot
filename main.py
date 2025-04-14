import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

URL = os.getenv("JOB_URL")
KEYWORDS = os.getenv("JOB_KEYWORDS").split(",")

def send_email(subject, body):
    sender = os.getenv("SENDER_EMAIL")
    receiver = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
        print("✅ Email sent!")

def check_jobs():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    jobs = soup.find_all("h2")  # Adjust based on actual job titles' tag

    for job in jobs:
        job_title = job.get_text(strip=True).lower()
        if any(keyword in job_title for keyword in KEYWORDS):
            # Create last_alert.txt if it doesn't exist
            if not os.path.exists("last_alert.txt"):
                with open("last_alert.txt", "w") as f:
                    pass  # Create empty file

            # Check if job is new
            with open("last_alert.txt", "r+") as f:
                if job_title not in f.read():
                    send_email("New Fresher Job at ClickPost", f"New opening: {job_title}\n\nCheck: {URL}")
                    f.write(f"{job_title}\n")
            break

if __name__ == "__main__":
    print("🔍 Checking for new job postings...")
    check_jobs()
    print("✓ Job check complete")
