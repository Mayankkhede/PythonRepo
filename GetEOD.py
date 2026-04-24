from jira import JIRA
from datetime import datetime

# --- 1. CONFIGURATION ---
JIRA_URL = "https://mayankkhede.atlassian.net"
EMAIL = "mayankkhede0000@gmail.com"
# Keeping your token here as per your request
API_TOKEN = "ATATT3xFfGF0TDq4eyk13WiIXTJvxC6kE-rHSKVfi7LlynP45Lusf6KIgx7FuSftXWH7ePRB_6vrVRebo3_lop8E3wp7BKipQ8YKIvGhiPS8ZUQAf4OEuYw_P-pw_IyBJQC4K8QlmKkFlb4MXxaM3HYeIYfWwPxaOHYrlPe_tmRjnqV7Ba_SbJw=0B5A690C" 
PROJECT_KEY = "LOGI"

# --- 2. CONNECT ---
jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

def get_eod_report():
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 3. IMPROVED JQL 
    # Added "Story" and "Bug" to the list just in case the long names are causing the zero results
    jql = (f'project = {PROJECT_KEY} '
           f'AND issuetype IN ("UserStory (Feature Enhancement)", "Bug/Defect", "Technical Debt", "Story", "Bug") '
           f'AND status IN ("QA-COMPLETED", "Completed", "DEV-ASSIGNED", "Closed", "QA-INPROGRESS", "QA-ONHOLD", "DEV-ASSI") '
           f'AND updated >= "{today_str}" '
           f'AND assignee = currentUser() '
           f'ORDER BY updated DESC')

    print(f"--- EOD Activity Report: {today_str} ---")
    
    try:
        print("Searching Jira...")
        issues = jira.search_issues(jql, maxResults=50)
        print(f"Total issues found with today's activity: {len(issues)}\n")
        
        if not issues:
            print(f"Check if you have tickets assigned to you with updates on {today_str}.")
            return

        for issue in issues:
            key = issue.key
            summary = issue.fields.summary
            status_name = issue.fields.status.name.upper()
            
            # --- 4. STATUS LOGIC ---
            is_completed = status_name in ['QA-COMPLETED', 'COMPLETED', 'CLOSED']
            
            reported_sub_issues = []
            
            if not is_completed:
                # Checking for "Sub Issue" children
                subtasks = getattr(issue.fields, "subtasks", [])
                for sub in subtasks:
                    # We fetch the child to check its type
                    child = jira.issue(sub.key)
                    if child.fields.issuetype.name == "Sub Issue":
                        reported_sub_issues.append(f"{child.key} : {child.fields.summary}")

            # --- 5. FINAL FORMATTING ---
            print(f"{key} : {summary}")

            if is_completed:
                print(f"Status: QA-completed\n")
            elif reported_sub_issues:
                print(f"Status: In-progress and reported below issues")
                for item in reported_sub_issues:
                    print(f"   {item}")
                print("") 
            else:
                print(f"Status: In-progress and no issue reported\n")

    except Exception as e:
        print(f"Error executing agent: {e}")

if __name__ == "__main__":
    get_eod_report()