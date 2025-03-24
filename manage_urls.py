#!/usr/bin/env python3

import json
import os
from datetime import datetime

def load_url_records(records_file='signed_urls.json'):
    """Load existing URL records from JSON file"""
    try:
        with open(records_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No URL records found")
        return {}

def save_url_records(records, records_file='signed_urls.json'):
    """Save URL records to JSON file"""
    with open(records_file, 'w') as f:
        json.dump(records, f, indent=2)

def get_url_status(expiration_str):
    """Get status and remaining days for a URL"""
    expiration = datetime.fromisoformat(expiration_str)
    current_time = datetime.now()
    
    if current_time > expiration:
        return "EXPIRED", 0
    else:
        days_left = (expiration - current_time).days
        return "VALID", days_left

def display_urls(records):
    """Display all URLs with their status"""
    if not records:
        print("\nNo URLs found in the records.")
        return False

    print("\nStored URLs:")
    print("-" * 100)
    print(f"{'Index':<6} {'Status':<8} {'Days Left':<10} {'Filename':<30} {'Previous URLs':<10}")
    print("-" * 100)

    for idx, (filename, record) in enumerate(records.items(), 1):
        status, days_left = get_url_status(record['expiration'])
        status_color = '\033[92m' if status == "VALID" else '\033[91m'  # Green for valid, Red for expired
        history_count = len(record.get('history', []))
        print(f"{idx:<6} {status_color}{status}\033[0m{'':<2} {days_left:<10} {filename:<30} {history_count} previous")
    
    return True

def show_url_history(records, filename):
    """Display history of URLs for a specific file"""
    if filename not in records:
        print(f"\nNo record found for {filename}")
        return

    record = records[filename]
    history = record.get('history', [])
    
    print(f"\nURL History for {filename}:")
    print("-" * 80)
    print("Current URL:")
    status, days_left = get_url_status(record['expiration'])
    print(f"Status: {status} (Days left: {days_left})")
    print(f"Created: {record['created_at']}")
    print(f"URL: {record['url']}")
    
    if history:
        print("\nPrevious URLs:")
        for i, old_url in enumerate(reversed(history), 1):
            status, _ = get_url_status(old_url['expiration'])
            print(f"\n{i}. Status: {status}")
            print(f"   Created: {old_url['created_at']}")
            print(f"   URL: {old_url['url']}")
    else:
        print("\nNo previous URLs")

def delete_urls(records):
    """Interactive URL deletion"""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        
        if not display_urls(records):
            return records

        print("\nOptions:")
        print("1. Delete specific URL(s)")
        print("2. Delete all expired URLs")
        print("3. Delete all URLs")
        print("4. Show URL history")
        print("5. Back to main menu")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            indices = input("\nEnter URL numbers to delete (comma-separated, e.g., 1,3,4): ").strip()
            try:
                # Convert input to list of integers
                to_delete = [int(i.strip()) for i in indices.split(',')]
                # Get list of filenames
                filenames = list(records.keys())
                # Delete selected URLs
                for idx in sorted(to_delete, reverse=True):
                    if 1 <= idx <= len(filenames):
                        filename = filenames[idx-1]
                        del records[filename]
                        print(f"\nDeleted URL for: {filename}")
                input("\nPress Enter to continue...")
            except ValueError:
                print("\nInvalid input. Please enter numbers separated by commas.")
                input("Press Enter to continue...")

        elif choice == '2':
            # Delete expired URLs
            initial_count = len(records)
            records = {
                filename: record
                for filename, record in records.items()
                if get_url_status(record['expiration'])[0] == "VALID"
            }
            deleted_count = initial_count - len(records)
            print(f"\nDeleted {deleted_count} expired URL(s)")
            input("Press Enter to continue...")

        elif choice == '3':
            confirm = input("\nAre you sure you want to delete ALL URLs? (yes/no): ").lower()
            if confirm == 'yes':
                records.clear()
                print("\nAll URLs have been deleted.")
            input("Press Enter to continue...")

        elif choice == '4':
            idx = input("\nEnter URL number to show history: ").strip()
            try:
                idx = int(idx)
                if 1 <= idx <= len(records):
                    filename = list(records.keys())[idx-1]
                    show_url_history(records, filename)
                    input("\nPress Enter to continue...")
                else:
                    print("\nInvalid URL number")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
                input("Press Enter to continue...")

        elif choice == '5':
            break

        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

    return records

def main():
    records_file = 'signed_urls.json'
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen
        
        records = load_url_records(records_file)
        
        print("\nURL Management Tool")
        print("=" * 20)
        print("1. View URLs")
        print("2. Manage/Delete URLs")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == '1':
            display_urls(records)
            input("\nPress Enter to continue...")

        elif choice == '2':
            updated_records = delete_urls(records)
            save_url_records(updated_records, records_file)

        elif choice == '3':
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 