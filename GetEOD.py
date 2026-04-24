import smtplib
from email.message import EmailMessage
from jira import JIRA
from datetime import datetime

# --- 1. CONFIGURATION ---
JIRA_URL = "https://mayankkhede.atlassian.net"
EMAIL = "mayankkhede0000@gmail.com"
API_TOKEN = "ATATT3xFfGF0TDq4eyk13WiIXTJvxC6kE-rHSKVfi7LlynP45Lusf6KIgx7FuSftXWH7ePRB_6vrVRebo3_lop8E3wp7BKipQ8YKIvGhiPS8ZUQAf4OEuYw_P-pw_IyBJQC4K8QlmKkFlb4MXxaM3HYeIYfWwPxaOHYrlPe_tmRjnqV7Ba_SbJw=0B5A690C" 
PROJECT_KEY = "LOGI"

# --- 2. CONNECT ---
jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

def send_email(report_text, file_name):
    """Function to send the generated report via Gmail"""
    sender_email = "mayankkhede0000@gmail.com"
    # Note: Use your 16-character Google App Password here
    sender_password = "gmqt gvul rksj qtvf" 
    recipient_email = "c-mayank.khede@on24.com"

    msg = EmailMessage()
    msg["Subject"] = f"Jira EOD Report - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(report_text)

    try:
        # Attach the text file as well
        with open(file_name, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=file_name)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls() # Secure the connection
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("✅ Email sent successfully to", recipient_email)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def get_eod_report():
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    jql = (f'project = {PROJECT_KEY} '
           f'AND issuetype IN ("UserStory (Feature Enhancement)", "Bug/Defect", "Technical Debt", "Story", "Bug") '
           f'AND status IN ("QA-COMPLETED", "Completed", "DEV-ASSIGNED", "Closed", "QA-INPROGRESS", "QA-ONHOLD", "DEV-ASSI") '
           f'AND updated >= "{today_str}" '
           f'AND assignee = currentUser() '
           f'ORDER BY updated DESC')

    # Initialize a string to build the email body
    full_report_body = f"Hello Team,\n\nBelow are the Jira items for today ({today_str}):\n\n"
    
    print(f"--- EOD Activity Report: {today_str} ---")
    
    try:
        print("Searching Jira...")
        issues = jira.search_issues(jql, maxResults=50)
        
        if not issues:
            print(f"No tasks found for today.")
            return

        for issue in issues:
            key = issue.key
            summary = issue.fields.summary
            status_name = issue.fields.status.name.upper()
            
            is_completed = status_name in ['QA-COMPLETED', 'COMPLETED', 'CLOSED']
            reported_sub_issues = []
            
            if not is_completed:
                subtasks = getattr(issue.fields, "subtasks", [])
                for sub in subtasks:
                    child = jira.issue(sub.key)
                    if child.fields.issuetype.name == "Sub Issue":
                        reported_sub_issues.append(f"{child.key} : {child.fields.summary}")

            # Append to the report string
            issue_header = f"{key} : {summary}\n"
            full_report_body += issue_header
            print(issue_header, end="")

            if is_completed:
                status_text = "Status: QA-completed\n\n"
                full_report_body += status_text
                print(status_text, end="")
            elif reported_sub_issues:
                status_text = "Status: In-progress and reported below issues:\n"
                full_report_body += status_text
                print(status_text, end="")
                for item in reported_sub_issues:
                    full_report_body += f"   {item}\n"
                    print(f"   {item}")
                full_report_body += "\n"
                print("")
            else:
                status_text = "Status: In-progress and no issue reported\n\n"
                full_report_body += status_text
                print(status_text, end="")

        full_report_body += "Thanks,\nMayank"

        # 1. Save report to a local file
        file_name = f"Jira_EOD_{today_str}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(full_report_body)

        # 2. Trigger the Email
        send_email(full_report_body, file_name)

    except Exception as e:
        print(f"Error executing agent: {e}")

if __name__ == "__main__":
    get_eod_report()