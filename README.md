# Jira Issues Extraction and Reporting

This script extracts Jira issues using the Jira API, stores them in a SQLite database, and generates summary reports in Excel format.

## Features
- Connects to Jira using API credentials
- Extracts issues using JQL (Jira Query Language)
- Stores issue data in SQLite database
- Generates an Excel summary report with issue type counts
- Creates a detailed Excel report with issue keys and summaries

## Requirements
Ensure you have the following Python libraries installed:

sh
pip install pandas sqlite3 xlsxwriter jira openpyxl


## Configuration
Update the following variables in the script to match your Jira environment:

python
EMAIL = 'name@domain.com'  # Jira username
API_TOKEN = 'api_token'  # Jira API token
SERVER = 'https://project.atlassian.net/'  # Jira server URL
JQL = 'project = project_name'  # JQL Query


## Usage
Run the script using Python:

sh
python script.py


## Output
- `jira_issues.db`: SQLite database storing the extracted Jira issues.
- `jira_summary.xlsx`: Excel file containing a summary of issues by type.
- `jira_report.xlsx`: Excel file listing issue keys and summaries.

## Error Handling
If the script fails to connect to Jira, it will print an error message and exit.

## License
This project is licensed under the MIT License.

