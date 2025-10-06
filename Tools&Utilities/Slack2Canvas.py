"""
 Slack2Canvas Bot 

Purpose:
- Compare Canvas course roster with Slack workspace.
- Identify missing users and handle fuzzy name mismatches.
- Automatically invite missing users via Microsoft Graph (optional).
- Generate CSV reports for manual review.

Modes:
- csv_only: Generate only CSV report of possible mismatches.
- auto_invite: Send invites to unmatched users and generate CSV.

Before Implementation:
- Obtain API access and secrets (see below).
- Ensure Slack workspace uses SSO with SLU email for better matching.
- Verify Canvas API token has read access to course enrollments.
- Verify Microsoft Graph app has permission to send emails/invites.
"""

# ---------------------------
# IMPORTS
# ---------------------------
# import requests
# import pandas as pd
# import sys
# from slack_sdk import WebClient
# from msal import ConfidentialClientApplication
# from fuzzywuzzy import fuzz

# ---------------------------
# MODE SELECTION
# ---------------------------
# mode = sys.argv[1] if len(sys.argv) > 1 else "csv_only"
# Validate mode: csv_only or auto_invite

# ---------------------------
# GITHUB SECRETS NEEDED
# ---------------------------
# Canvas API
#   - CANVAS_API_TOKEN: Canvas access token
#   - CANVAS_DOMAIN
#   - COURSE_ID: Canvas course ID

# Slack API
#   - SLACK_BOT_TOKEN: Bot token with "users:read.email" scope
#   - SLACK_INVITE_LINK: Link for inviting users (if needed)

# Microsoft Graph API
#   - GRAPH_CLIENT_ID: App ID
#   - GRAPH_CLIENT_SECRET: App secret
#   - GRAPH_TENANT_ID: Tenant ID for OAuth
#   - BOT_EMAIL: Email address used to send invites

# Output
#   - OUTPUT_DIR: Directory to store CSV reports

# ---------------------------
# FUNCTIONS TO IMPLEMENT
# ---------------------------

# 1. fetch_canvas_course_enrollments()

# 2. fetch_slack_users()

# 3. get_graph_app_token()

# 4. send_graph_invite(email)

# 5. compare_users()

# 6. save_csv_reports()


# ---------------------------
# MAIN FUNCTION
# ---------------------------
# def main():
#   - Create output directory
#   - Fetch Canvas users
#   - Fetch Slack users
#   - Compare users
#   - Send invites if mode is auto_invite
#   - Save CSV reports

# ---------------------------
# RUN SCRIPT
# ---------------------------
# if __name__ == "__main__":
#     main()

"""
Before Building Checklist:
1. Obtain Canvas API token: 
   - Log into Canvas > Account > Settings > Approved Integrations > Generate new token.
2. Verify Slack bot:
   - Create Slack app in workspace
   - Request "users:read.email" scope
   - Install app to workspace
   - Copy Bot OAuth token into GitHub secret SLACK_BOT_TOKEN
3. Microsoft Graph:
   - Register app in Azure AD
   - Grant "Mail.Send" permissions
   - Get Client ID, Secret, Tenant ID
   - Set BOT_EMAIL to the email account authorized to send invites
4. Create GitHub Secrets for all tokens and IDs
5. Configure workflow_dispatch in GitHub Actions for manual run
"""
