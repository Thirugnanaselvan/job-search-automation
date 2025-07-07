import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# Get credentials safely from environment
EMAIL_USER = os.environ.get("jobapplicationsforthiru@gmail.com")
EMAIL_PASS = os.environ.get("ybag rhzf obnc olhr")
TO_EMAIL   = os.environ.get("jobapplicationsforthiru@gmail.com")

# Configurations
KEYWORDS = ["software developer", "python developer", "web developer", "software analyst"]
LOCATIONS = ["bangalore", "chennai"]

# Fetch jobs from Indeed
def fetch_jobs():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for keyword in KEYWORDS:
        for location in LOCATIONS:
            url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            for div in soup.find_all('div', class_='job_seen_beacon')[:5]:
                title = div.find('h2').text.strip() if div.find('h2') else "No title"
                company = div.find('span', class_='companyName').text.strip() if div.find('span', class_='companyName') else "Unknown"
                snippet = div.find('div', class_='job-snippet').text.strip() if div.find('div', class_='job-snippet') else ""
                link_tag = div.find('a')
                link = f"https://www.indeed.com{link_tag.get('href')}" if link_tag else "#"
                jobs.append({
                    "title": title,
                    "company": company,
                    "desc": snippet,
                    "link": link
                })
    return jobs

# Create LinkedIn outreach message
def generate_linkedin_message(job):
    return f"""
Hi [Recruiter/HR],

I came across the opening for {job['title']} at {job['company']} on Indeed. I am an enthusiastic fresher with skills in Python, web & software development. 

Would love to connect and explore how I could contribute.

Regards,
Thirugnanaselvan
"""

# Send the email
def send_email(jobs):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📝 Daily Fresher Job Digest - {datetime.date.today()}"
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL

    # Build the HTML content
    html = "<h2>Today's Job Opportunities</h2><table border='1' cellpadding='5' cellspacing='0'>"
    html += "<tr><th>Title</th><th>Company</th><th>Description</th><th>Link</th></tr>"
    for job in jobs:
        html += f"<tr><td>{job['title']}</td><td>{job['company']}</td><td>{job['desc']}</td><td><a href='{job['link']}'>Apply</a></td></tr>"
    html += "</table><br>"

    # LinkedIn messages
    html += "<h3>Suggested LinkedIn Outreach Messages:</h3><ul>"
    for job in jobs:
        html += f"<li><pre>{generate_linkedin_message(job)}</pre></li>"
    html += "</ul>"

    msg.attach(MIMEText(html, 'html'))

    # Send it
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())

# Main run
def main():
    print("🔍 Fetching jobs...")
    jobs = fetch_jobs()
    print(f"✅ Found {len(jobs)} jobs. Sending email...")
    send_email(jobs)
    print("📬 Email sent successfully!")

if __name__ == "__main__":
    main() 