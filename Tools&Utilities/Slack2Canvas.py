"""
CSV-based Canvas Roster to Slack User Matcher

CSV Score Rules:
1. Same name and same @slu.edu email -> best_match_score = 10, reason = "same name, same @slu.edu email"
2. Same name and different domain email -> best_match_score = 50, reason = "same name, different domain email"
3. Otherwise → compute fuzzy name match -> best_match_score = fuzzy ratio, reason = "fuzzy name match"

Dependencies:
    pip install slack_sdk pandas fuzzywuzzy python-Levenshtein python-dotenv

Usage:
    Make a .env file with:
        CANVAS_CSV_PATH={path to Canvas CSV file}
        SLACK_BOT_TOKEN={Slack Bot Token with users:read scope and users:read.email scope}
        OUTPUT_DIR={directory to save output CSV}
"""

import os
import sys
import pandas as pd
from slack_sdk import WebClient
from fuzzywuzzy import fuzz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  

# Config from environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANVAS_CSV_PATH = os.getenv("CANVAS_CSV_PATH")  # CSV file with columns: name,email
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
FUZZY_THRESHOLD = 85  # minimum similarity to count as possible match


# Helpers
def norm_email(e):
    """Normalize emails by trimming and lowercasing."""
    return e.strip().lower() if e else ""

# Canvas CSV Loader
def fetch_canvas_users_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    df["email"] = df["email"].apply(norm_email)
    df["name"] = df["name"].str.strip().str.lower()
    return df

# Slack API Loader
def fetch_slack_users(token):
    """Fetch all Slack users (excluding bots and deleted accounts)."""
    client = WebClient(token=token)
    users = []
    cursor = None

    while True:
        resp = client.users_list(limit=200, cursor=cursor)
        if not resp["ok"]:
            sys.exit(1)

        for member in resp["members"]:
            if member.get("deleted") or member.get("is_bot"):
                continue
            profile = member.get("profile", {}) or {}
            email = profile.get("email")
            users.append({
                "name": (profile.get("real_name") or "").strip().lower(),
                "email": norm_email(email)
            })

        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return users

# Scoring rules
def get_custom_score_and_reason(canvas_name, canvas_email, slack_name, slack_email):
    """Apply CSV score rules."""
    canvas_domain = canvas_email.split("@")[-1] if "@" in canvas_email else ""
    slack_domain = slack_email.split("@")[-1] if slack_email else ""

    if canvas_name == slack_name:
        if canvas_domain == "slu.edu" and slack_domain == "slu.edu":
            return 10, "same name, same @slu.edu email"
        else:
            return 50, "same name, different domain email"
    return None, ""

# Main workflow
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    canvas_df = fetch_canvas_users_from_csv(CANVAS_CSV_PATH)
    slack_users = fetch_slack_users(SLACK_BOT_TOKEN)

    slack_info = [(u["name"], u["email"]) for u in slack_users]
    slack_emails = {u["email"] for u in slack_users if u.get("email")}
    slack_names = [u["name"] for u in slack_users if u.get("name")]

    possible_mismatches = []

    for idx, row in canvas_df.iterrows():
        canvas_name = row["name"]
        canvas_email = row["email"]

        # Skip if email is already in Slack
        if canvas_email in slack_emails:
            continue

        best_score = 0
        match_reason = ""

        # Checking custom rules first
        for sname, semail in slack_info:
            score, reason = get_custom_score_and_reason(canvas_name, canvas_email, sname, semail)
            if score is not None:
                best_score = score
                match_reason = reason
                break  

        # Use fuzzy matching if no custom rule apply
        if best_score == 0 and slack_names:
            fuzzy_scores = [fuzz.ratio(canvas_name, sname) for sname in slack_names]
            best_score = max(fuzzy_scores)
            match_reason = "fuzzy name match"

        possible_mismatches.append({
            "canvas_name": canvas_name,
            "canvas_email": canvas_email,
            "best_match_score": best_score,
            "match_reason": match_reason
        })

    # Save the CSV report
    csv_path = os.path.join(OUTPUT_DIR, "possible_mismatches.csv")
    pd.DataFrame(possible_mismatches).to_csv(csv_path, index=False)

    print("Processing complete")


if __name__ == "__main__":
    main()
