import pandas as pd
import sqlite3
import xlsxwriter
from jira import JIRA
from openpyxl import Workbook

# Settings
EMAIL = 'name@domain.com'  # Jira username
API_TOKEN = 'api_token'  # Jira API token
SERVER = 'https://project.atlassian.net/'  # Jira server URL
JQL = 'project = project_name'  # JQL Query

# Establish Jira connection
try:
    jira = JIRA(options={'server': SERVER}, basic_auth=(EMAIL, API_TOKEN))
    jira_issues = jira.search_issues(JQL, maxResults=False)
except Exception as e:
    print(f'Error connecting to Jira: {e}')
    exit(1)

# Extract issues into a DataFrame
issues_data = [{
    'id': issue.id,
    'key': issue.key,
    'self': issue.self,
    'assignee': str(issue.fields.assignee),
    'creator': str(issue.fields.creator),
    'reporter': str(issue.fields.reporter),
    'created': str(issue.fields.created),
    'labels': str(issue.fields.labels),
    'components': str(issue.fields.components),
    'description': str(issue.fields.description),
    'summary': str(issue.fields.summary),
    'fixVersions': str(issue.fields.fixVersions),
    'issuetype': str(issue.fields.issuetype.name),
    'priority': str(issue.fields.priority.name),
    'project': str(issue.fields.project),
    'resolution': str(issue.fields.resolution),
    'resolution_date': str(issue.fields.resolutiondate),
    'status': str(issue.fields.status.name),
    'updated': str(issue.fields.updated),
    'versions': str(issue.fields.versions),
    'subtask': str(issue.fields.issuetype.subtask),
    'status_description': str(issue.fields.status.description),
    'watchcount': str(issue.fields.watches.watchCount),
} for issue in jira_issues]

issues_df = pd.DataFrame(issues_data)

# Save to SQLite
with sqlite3.connect('jira_issues.db') as con:
    issues_df.to_sql('issues', con, if_exists='replace', index=False)
    print('Data successfully stored in SQLite.')

# Query summary from SQLite
with sqlite3.connect('jira_issues.db') as con:
    df_summary = pd.read_sql_query('SELECT issuetype, COUNT(*) AS count FROM issues GROUP BY issuetype', con)

# Create Excel summary
workbook = xlsxwriter.Workbook('jira_summary.xlsx')
worksheet = workbook.add_worksheet('Summary')
header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D8E4BC'})
center_format = workbook.add_format({'align': 'center'})

worksheet.write(0, 0, 'Issue Type', header_format)
worksheet.write(0, 1, 'Count', header_format)

for row_idx, (issue_type, count) in enumerate(zip(df_summary['issuetype'], df_summary['count']), start=1):
    worksheet.write(row_idx, 0, issue_type)
    worksheet.write(row_idx, 1, int(count), center_format)

workbook.close()
print('Summary Excel file created.')

# Generate a detailed report
wb = Workbook()
ws = wb.active
ws.append(['Key', 'Summary'])

for issue in issues_data:
    ws.append([issue['key'], issue['summary']])

wb.save('jira_report.xlsx')
print('Detailed Jira report saved.')
