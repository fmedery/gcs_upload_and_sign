#!/usr/bin/env python3

import json
from datetime import datetime

def check_all_urls(records_file='signed_urls.json'):
    """Check all stored URLs and remove expired ones"""
    try:
        with open(records_file, 'r') as f:
            records = json.load(f)
    except FileNotFoundError:
        print("No URL records found")
        return

    current_time = datetime.now()
    expired = []
    valid = []

    # Check each URL
    for filename, record in records.items():
        expiration = datetime.fromisoformat(record['expiration'])
        if current_time > expiration:
            expired.append(filename)
        else:
            days_left = (expiration - current_time).days
            valid.append((filename, days_left))

    # Remove expired URLs
    for filename in expired:
        del records[filename]

    # Save updated records
    with open(records_file, 'w') as f:
        json.dump(records, f, indent=2)

    # Print report
    print("\nURL Status Report:")
    print("-----------------")
    if valid:
        print("\nValid URLs:")
        for filename, days in valid:
            print(f"- {filename}: {days} days remaining")
    
    if expired:
        print("\nExpired URLs (removed):")
        for filename in expired:
            print(f"- {filename}")

if __name__ == "__main__":
    check_all_urls() 