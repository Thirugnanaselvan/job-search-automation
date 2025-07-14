import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------------------------
# 🎯 Search criteria (union + intersection)
# ---------------------------------------
ROLE_SYNONYMS = ["software developer", "software development", "software engineer", "sde"]
JOB_TYPE = ["full time"]
EXPERIENCE_LEVELS = ["fresher", "entry level", "junior", "intern"]
LOCATIONS = ["chennai", "bangalore", "bengaluru", "tamilnadu"]
SKILLS = [
    "python development", "html/css developer", "javascript developer",
    "react developer", "front-end developer", "web developer",
    "sql developer", "mern stack development"
]

# ---------------------------------------
# 🔥 Platforms (direct search links)
# ---------------------------------------
platforms = {
    "LinkedIn - Chennai": "https://www.linkedin.com/jobs/search/?keywords=software%20developer&location=Chennai%2C%20Tamil%20Nadu%2C%20India&f_E=1&f_TP=1",
    "LinkedIn - Bangalore": "https://www.linkedin.com/jobs/search/?keywords=software%20developer&location=Bengaluru%2C%20Karnataka%2C%20India&f_E=1&f_TP=1",
    "Naukri - Chennai": "https://www.naukri.com/fresher-software-developer-jobs-in-chennai",
    "Naukri - Bangalore": "https://www.naukri.com/fresher-software-developer-jobs-in-bangalore",
    "Indeed - Chennai": "https://www.indeed.co.in/jobs?q=software+developer+fresher&l=Chennai",
    "Indeed - Bangalore": "https://www.indeed.co.in/jobs?q=software+developer+fresher&l=Bangalore",
    "AngelList - India": "https://angel.co/jobs",
    "FreshersWorld": "https://www.freshersworld.com/jobs"
    "Hirist - Tech Jobs India": "https://www.hirist.tech/c/frontend-development-jobs?ref=homepagecat&minexp=0&maxexp=1&loc=Anywhere-in-India_Metros_Delhi-NCR_Delhi_Ghaziabad_Faridabad_Gurgaon%2FGurugram_Noida_Mumbai_Kolkata_Bangalore_Pune_Hyderabad_Chennai_Surat_Vishakhapatnam%2FVizag_Ahmedabad_Amritsar_Andhra-Pradesh_Aurangabad_Bhubaneshwar_Bihar_Chandigarh_Chhattisgarh_Cochin%2FKochi_Coimbatore_Cuttack_Dehradun_Gandhinagar_Goa_Greater-Noida_Gujarat_Guntur_Guwahati_Haridwar_Haryana_Hosur_Hubli_Jaipur_Jalandhar_Jammu_Jammu-%26-Kashmir_Jamshedpur_Jharkhand_Jodhpur_Karnataka_Kerala_Lucknow_Ludhiana_Madurai_Maharashtra_MP_Mysore_Nagpur_Nasik_Navi-Mumbai_Odisha_Panipat_Patiala_Patna_Pondicherry_Punjab_Raipur_Rajasthan_Rajkot_Ranchi_Sonipat_Srinagar_Tamil-Nadu_Telangana_Thane_Trivandrum%2FThiruvananthapuram_Udaipur_UP_Uttarakhand_Vadodara%2FBaroda_Varanasi%2FBanaras_Vijayawada_Warangal_Arunachal-Pradesh_Assam_Bhopal_Indore_Manipur_Meghalaya_Mizoram_Nagaland_Tripura_West-Bengal_Mohali&posting=3",
    "Foundit (ex Monster)": "https://www.foundit.in",
    "Glassdoor India": "https://www.glassdoor.co.in/Job/india-software-developer-jobs-SRCH_IL.0,5_IN115_KO6,25.htm",
    "Google Careers India": "https://careers.google.com/locations/india/",
    "Superset": "https://joinsuperset.com"
}

# ---------------------------------------
# 🔥 Company career pages
# ---------------------------------------
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

# ---------------------------------------
# 🔍 Smart job match function
# ---------------------------------------
def job_matches(text):
    return (
        any(word in text for word in ROLE_SYNONYMS) and
        any(word in text for word in JOB_TYPE) and
        any(word in text for word in EXPERIENCE_LEVELS) and
        any(word in text for word in LOCATIONS) and
        any(word in text for word in SKILLS)
    )

# ---------------------------------------
# 🔍 Check platforms & company sites
# ---------------------------------------
def check_sites():
    # Check platforms
    for name, url in platforms.items():
        print(f"🔍 Checking {name}")
        try:
            response = requests.get(url, timeout=10)
            text = response.text.lower()
            if job_matches(text):
                found_jobs.append((name, url))
        except Exception as e:
            print(f"⚠️ Error with {name}: {e}")

    # Check company career sites
    for company, url in companies.items():
        print(f"🔍 Checking {company}")
        try:
            response = requests.get(url, timeout=10)
            text = response.text.lower()
            if job_matches(text):
                found_jobs.append((company, url))
        except Exception as e:
            print(f"⚠️ Error with {company}: {e}")

# ---------------------------------------
# ✉️ Send email with job results
# ---------------------------------------
def send_email(jobs):
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")
    TO_EMAIL   = os.environ.get("TO_EMAIL")

    if not (EMAIL_USER and EMAIL_PASS and TO_EMAIL):
        print("⚠️ Missing email environment variables.")
        return

    message_body = "<h2>📰 Matching Job Openings:</h2><ul>"
    for name, url in jobs:
        message_body += f"<li><strong>{name}</strong>: <a href='{url}'>{url}</a></li>"
    message_body += "</ul>"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = "🚀 New Matching Software / Web Dev Jobs in Chennai, Bangalore, Tamil Nadu"

    msg.attach(MIMEText(message_body, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")

# ---------------------------------------
# 🚀 Main execution
# ---------------------------------------
def main():
    check_sites()
    if found_jobs:
        print("✅ Matching jobs found. Sending email...")
        send_email(found_jobs)
    else:
        print("😴 No matching jobs today. No email sent.")

if __name__ == "__main__":
    main()
