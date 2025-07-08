import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --------------------------
# ✅ Configuration
# --------------------------
LOCATIONS = ["chennai", "bangalore", "hosur"]
EXPERIENCE_KEYWORDS = ["fresher", "intern"]
ROLE_KEYWORDS = ["software developer", "web developer", "python developer", "software analyst"]

# ✅ Platforms (job boards)
platforms = {
    "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords=software%20developer%20fresher&location=India",
    "Naukri": "https://www.naukri.com/fresher-software-developer-jobs-in-india",
    "Indeed": "https://www.indeed.co.in/jobs?q=software+developer+fresher&l=India",
    "Foundit": "https://www.foundit.in",
    "AngelList": "https://angel.co/jobs",
    "CutShort": "https://cutshort.io/jobs",
    "Instahyre": "https://www.instahyre.com",
    "Hirect": "https://hirect.in",
    "FreshersWorld": "https://www.freshersworld.com/jobs",
    "Glassdoor": "https://www.glassdoor.co.in/Job/india-software-developer-jobs-SRCH_IL.0,5_IN115_KO6,25.htm",
    "TimesJobs": "https://www.timesjobs.com",
    "HackerRank": "https://www.hackerrank.com/jobs",
    "HackerEarth": "https://www.hackerearth.com/challenges/hiring/",
    "StackOverflow": "https://stackoverflow.com/jobs?l=India"
}

# ✅ Company career sites
companies = {
    "TCS": "https://www.tcs.com/careers",
    "Infosys": "https://career.infosys.com",
    "Wipro": "https://careers.wipro.com",
    "Cognizant": "https://careers.cognizant.com",
    "Capgemini": "https://www.capgemini.com/in-en/careers/",
    "HCL": "https://www.hcltech.com/careers",
    "Zoho": "https://careers.zohocorp.com",
    "Freshworks": "https://www.freshworks.com/company/careers/",
    "ThoughtWorks": "https://www.thoughtworks.com/careers",
    "Flipkart": "https://www.flipkartcareers.com",
    "Paytm": "https://paytm.com/about-us/work",
    "Swiggy": "https://careers.swiggy.com",
    "Ola": "https://careers.olacabs.com",
    "Razorpay": "https://razorpay.com/jobs/",
    "Amazon": "https://www.amazon.jobs/en/locations/india",
    "Google": "https://careers.google.com/locations/india/",
    "Microsoft": "https://careers.microsoft.com",
    "IBM": "https://www.ibm.com/in-en/employment/",
    "Deloitte": "https://jobs2.deloitte.com/in/en"
}

found_jobs = []

# --------------------------
# 🔍 Job search logic
# --------------------------
def check_sites():
    # Check job platforms
    for name, url in platforms.items():
        print(f"🔍 Checking {name}")
        try:
            response = requests.get(url, timeout=10)
            text = response.text.lower()
            if (any(exp in text for exp in EXPERIENCE_KEYWORDS) and
                any(role in text for role in ROLE_KEYWORDS) and
                any(loc in text for loc in LOCATIONS)):
                found_jobs.append((name, url))
        except Exception as e:
            print(f"⚠️ Error with {name}: {e}")

    # Check company career sites
    for company, url in companies.items():
        print(f"🔍 Checking {company}")
        try:
            response = requests.get(url, timeout=10)
            text = response.text.lower()
            if (any(exp in text for exp in EXPERIENCE_KEYWORDS) and
                any(role in text for role in ROLE_KEYWORDS) and
                any(loc in text for loc in LOCATIONS)):
                found_jobs.append((company, url))
        except Exception as e:
            print(f"⚠️ Error with {company}: {e}")

# --------------------------
# ✉️ Email sender
# --------------------------
def send_email(jobs):
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")
    TO_EMAIL   = os.environ.get("TO_EMAIL")

    if not (EMAIL_USER and EMAIL_PASS and TO_EMAIL):
        print("⚠️ Missing email environment variables. Exiting.")
        return

    # Email body
    message_body = "<h2>📰 New Job Openings Matching Your Profile:</h2><ul>"
    for name, url in jobs:
        message_body += f"<li><strong>{name}</strong>: <a href='{url}'>{url}</a></li>"
    message_body += "</ul>"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = "🚀 New Fresher/Intern Software Jobs in Chennai, Bangalore, Hosur"

    msg.attach(MIMEText(message_body, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")

# --------------------------
# 🚀 Main flow
# --------------------------
def main():
    check_sites()
    if found_jobs:
        print("✅ Matching jobs found. Sending email...")
        send_email(found_jobs)
    else:
        print("😴 No jobs matching criteria today. No email sent.")

if __name__ == "__main__":
    main()
