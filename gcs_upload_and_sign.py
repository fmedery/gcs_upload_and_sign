#!/usr/bin/env python3

import os
import re
import sys
import json
import pyperclip
from datetime import timedelta, datetime
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
from google.cloud import storage

# Load environment variables from .env file
env_path = Path('.env')
if env_path.exists():
    load_dotenv()
else:
    print("Warning: .env file not found. Make sure to copy .env.template to .env and configure it.")
    sys.exit(1)

def sanitize_filename(filename):
    """
    Sanitize the filename by:
    1. Converting to lowercase
    2. Removing special characters and spaces
    3. Replacing spaces with underscores
    """
    # Get the base name in case a path is provided
    base_name = os.path.basename(filename)
    # Split the filename and extension
    name, ext = os.path.splitext(base_name)
    
    # Convert to lowercase and replace spaces with underscores
    name = name.lower().replace(' ', '_')
    # Remove special characters except underscores and hyphens
    name = re.sub(r'[^a-z0-9_-]', '', name)
    
    return f"{name}{ext.lower()}"

def load_url_records(records_file='signed_urls.json'):
    """Load existing URL records from JSON file"""
    try:
        with open(records_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_url_record(filename, signed_url, expiration_date, records_file='signed_urls.json'):
    """Save URL record with expiration date and maintain history"""
    records = load_url_records(records_file)
    
    # If file exists, move current URL to history
    if filename in records:
        current_record = records[filename]
        if 'history' not in current_record:
            current_record['history'] = []
        
        # Add current URL to history
        current_record['history'].append({
            'url': current_record['url'],
            'created_at': current_record['created_at'],
            'expiration': current_record['expiration']
        })
        
        # Keep only last 5 historical URLs
        current_record['history'] = current_record['history'][-5:]
    
    # Create or update the record
    records[filename] = {
        'url': signed_url,
        'expiration': expiration_date.isoformat(),
        'created_at': datetime.now().isoformat(),
        'history': records.get(filename, {}).get('history', [])
    }
    
    with open(records_file, 'w') as f:
        json.dump(records, f, indent=2)

def check_url_expiration(filename, records_file='signed_urls.json'):
    """Check if URL for given filename is expired"""
    records = load_url_records(records_file)
    
    if filename not in records:
        return None, "No URL record found"
    
    record = records[filename]
    expiration = datetime.fromisoformat(record['expiration'])
    
    if datetime.now() > expiration:
        return False, "URL has expired"
    else:
        days_left = (expiration - datetime.now()).days
        return True, f"URL valid for {days_left} more days"

def upload_and_sign(file_path, bucket_name, credentials_path, folder_path=None):
    """
    Upload a file to GCS bucket and generate a signed URL
    Args:
        file_path: Path to the file to upload
        bucket_name: Name of the GCS bucket
        credentials_path: Path to the service account credentials file
        folder_path: Optional folder path within the bucket (e.g., 'folder1/subfolder2')
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)

    # Initialize the client with credentials
    storage_client = storage.Client.from_service_account_json(credentials_path)
    
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Sanitize the filename
    original_filename = os.path.basename(file_path)
    sanitized_filename = sanitize_filename(original_filename)
    
    # Construct the full blob path including folder if specified
    if folder_path:
        # Remove leading/trailing slashes and sanitize folder path
        folder_path = folder_path.strip('/')
        folder_parts = [sanitize_filename(part) for part in folder_path.split('/')]
        blob_path = '/'.join(folder_parts + [sanitized_filename])
        
        # Create an empty object to ensure folder exists (GCS doesn't have real folders)
        folder_marker = bucket.blob(f"{'/'.join(folder_parts)}/")
        if not folder_marker.exists():
            folder_marker.upload_from_string('')
    else:
        blob_path = sanitized_filename
    
    # Upload the file
    blob = bucket.blob(blob_path)
    
    print(f"\nUploading {original_filename} to {blob_path}...")
    
    # Simple upload without progress tracking
    blob.upload_from_filename(
        file_path,
        timeout=120,  # 2 minutes timeout
        checksum='md5'
    )
    
    print(f"File uploaded as: {blob_path}")
    
    # Calculate expiration date (7 days from now)
    expiration_date = datetime.now() + timedelta(days=7)
    
    # Generate signed URL (7 days is the maximum allowed time)
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(days=7),
        method="GET"
    )
    
    # Save URL record
    save_url_record(blob_path, signed_url, expiration_date)
    
    return signed_url, blob_path

def show_active_url(filename):
    """Display active URL for a file"""
    records = load_url_records()
    
    if filename not in records:
        print(f"No active URL found for: {filename}")
        return False
    
    record = records[filename]
    status, days_left = check_url_expiration(filename)
    
    print(f"\nActive URL for {filename}:")
    print("-" * 80)
    print(f"Status: {status}")
    print(f"Created: {record['created_at']}")
    if status:
        print(f"Days remaining: {days_left}")
    print(f"URL: {record['url']}")
    
    # Copy URL to clipboard if it's still valid
    if status:
        pyperclip.copy(record['url'])
        print("\nURL has been copied to clipboard!")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python upload_and_sign.py <file_path> [folder_path]")
        print("Example:")
        print("  python upload_and_sign.py myfile.pdf")
        print("  python upload_and_sign.py myfile.pdf folder1/subfolder2")
        sys.exit(1)
    
    # Get configuration from environment variables
    bucket_name = os.getenv('GCS_BUCKET_NAME')
    credentials_path = os.getenv('GCS_CREDENTIALS_PATH', './gcs_storage_key.json')
    
    # Validate required environment variables
    if not bucket_name:
        print("Error: GCS_BUCKET_NAME environment variable is required")
        print("Make sure to copy .env.template to .env and configure it")
        sys.exit(1)
    
    if not os.path.exists(credentials_path):
        print(f"Error: Credentials file not found at {credentials_path}")
        sys.exit(1)
    
    file_path = sys.argv[1]
    folder_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        signed_url, blob_path = upload_and_sign(file_path, bucket_name, credentials_path, folder_path)
        print("\nUpload successful!")
        print(f"Signed URL (valid for 7 days):\n{signed_url}")
        
        # Check and display URL status
        status, days_left = check_url_expiration(blob_path)
        print(f"\nStatus: {status}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 