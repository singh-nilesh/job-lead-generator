import json
from datetime import datetime, timedelta
import re


def load_json(path='config.json'):
    with open(path) as f:
        return json.load(f)


def extract_posting_date(posted_text):
    """
    Extract the actual posting date from various text formats like:
    """
    today = datetime.now().date()
    
    # Case 1: "n day/s ago"
    day_match = re.search(r'Posted (\d+) day', posted_text)
    if day_match:
        days_ago = int(day_match.group(1))
        posted_date = today - timedelta(days=days_ago)
        return posted_date.strftime('%Y-%m-%d')
    
    # Case 2: "few hours ago" or "n hour/s ago"
    elif "hour" in posted_text:
        return today.strftime('%Y-%m-%d')  # Today's date
    
    # Case 3: "n week/s ago"
    week_match = re.search(r'Posted (\d+) week', posted_text)
    if week_match:
        weeks_ago = int(week_match.group(1))
        days_ago = weeks_ago * 7  # Convert weeks to days
        posted_date = today - timedelta(days=days_ago)
        return posted_date.strftime('%Y-%m-%d')
    
    # Additional case: "Posted today"
    elif "today" in posted_text.lower():
        return today.strftime('%Y-%m-%d')
    
    # Additional case: "Posted yesterday"
    elif "yesterday" in posted_text.lower():
        yesterday = today - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
    
    # If no pattern matches, return the original text
    return posted_text
