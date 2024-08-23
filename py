import os
import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your GitHub personal access token and organization/user name
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_ORG = 'ABHISHEKRANA171994'

# GitHub API URL
GITHUB_API_URL = f'https://api.github.com/orgs/{GITHUB_ORG}/repos'

# Email Configuration
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Get current date and the date 3 days ago
current_date = datetime.now()
three_days_ago = current_date - timedelta(days=0)

def get_repositories():
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return []

def extract_email(repo_name):
    # Remove the prefix 'Test_' and the date suffix
    if repo_name.startswith('Test_'):
        parts = repo_name[5:].rsplit('_', 1)  # Split at the last underscore
        if len(parts) == 2:
            username = parts[0]  # This should give you the username part
            email = f'{username}@gmail.com'
            return email
    return None

def send_email(recipient_email, repo_name, created_at):
    # Create the email content
    subject = "Action Required: Repository Approaching 45-Day Retention Policy"
    body = f"""
    Dear {recipient_email},

    This is a reminder that the following repository is about to reach the 45-day retention policy:

    Repository Name: {repo_name}
    Created At: {created_at}

    According to our policy, repositories that are older than 45 days may be subject to deletion or archival. 
    If this repository is still in use, please take the necessary steps to ensure it is backed up or maintained.

    Steps you can take:
    1. Review the repository and determine if it is still needed.
    2. If you require an extension beyond the 45-day period, please contact the system administrator.
    3. Ensure that any important data within the repository is backed up.
    4. Consider archiving the repository if it is no longer active but you wish to retain it for reference.

    If you have any questions or need further assistance, please don't hesitate to reach out to the IT support team.

    Thank you for your attention to this matter.

    Best regards,
    [Your Name]
    [Your Company]
    """

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        print(f"Email sent to {recipient_email} successfully.")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

def check_repositories():
    repos = get_repositories()
    with open('repo_details.txt', 'w') as file:  # Open the file in write mode
        for repo in repos:
            repo_name = repo['name']
            if repo_name.startswith('Test_'):
                created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if created_at < three_days_ago:
                    email = extract_email(repo_name)
                    if email:
                        file.write(f"Repo name--{repo_name}\n")
                        file.write(f"Email--{email}\n")
                        file.write(f"Created At: {created_at}\n\n")
                        print(f"Repository: {repo_name}, Email: {email}, Created At: {created_at}")
                        send_email(email, repo_name, created_at)

if __name__ == '__main__':
    check_repositories()
