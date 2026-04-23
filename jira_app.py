import streamlit as st
from jira import JIRA

# 1. --- JIRA CONNECTION ---
# Replace with your fresh API Token for security
JIRA_URL = "https://mayankkhede.atlassian.net"
EMAIL = "mayankkhede0000@gmail.com"
API_TOKEN = "ATATT3xFfGF0TDq4eyk13WiIXTJvxC6kE-rHSKVfi7LlynP45Lusf6KIgx7FuSftXWH7ePRB_6vrVRebo3_lop8E3wp7BKipQ8YKIvGhiPS8ZUQAf4OEuYw_P-pw_IyBJQC4K8QlmKkFlb4MXxaM3HYeIYfWwPxaOHYrlPe_tmRjnqV7Ba_SbJw=0B5A690C" 

# Initialize Jira connection once
@st.cache_resource
def get_jira_connection():
    return JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

jira = get_jira_connection()

# 2. --- UI SETUP ---
st.set_page_config(page_title="Jira Test Agent", page_icon="🧪")
st.title("📋 Xray Test Navigator")
st.markdown("Select a component to fetch associated test scenarios.")

# 3. --- THE DROPDOWN (FEED LABELS HERE) ---
# Add all the labels you want to see in the dropdown list
component_labels = [
    "LOGI-7", 
    "API",
    "c3",
    "c-log-webcastsintelligencenurturereportpage"
]

selected_label = st.selectbox("Select Component Label:", component_labels)

# 4. --- SEARCH LOGIC ---
if st.button("Fetch Test Scenarios"):
    jql = f'project = "LOGI" AND type = "Test" AND labels = "{selected_label}" ORDER BY created DESC'
    
    with st.spinner(f"Searching Jira for {selected_label}..."):
        try:
            issues = jira.search_issues(jql, maxResults=50)
            
            if issues:
                st.success(f"Found {len(issues)} test cases.")
                
                for issue in issues:
                    # Using Expanders to keep the UI clean
                    with st.expander(f"{issue.key} : {issue.fields.summary}"):
                        st.write(f"**Status:** {issue.fields.status.name}")
                        st.write(f"**Priority:** {issue.fields.priority.name if issue.fields.priority else 'None'}")
                        
                        # Description logic: returns 'null' if empty as you requested
                        desc = issue.fields.description if issue.fields.description else "null"
                        st.write("**Description:**")
                        st.info(desc)
                        
                        st.markdown(f"[🔗 View in Jira]({JIRA_URL}/browse/{issue.key})")
            else:
                st.warning("No tests found with this label.")
                
        except Exception as e:
            st.error(f"Error running JQL: {e}")