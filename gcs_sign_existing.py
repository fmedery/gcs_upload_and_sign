#!/usr/bin/env python3

import os
from datetime import datetime, timedelta
from google.cloud import storage
from google.cloud.storage.blob import Blob
from dotenv import load_dotenv
import sys
import pyperclip

def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    
    bucket_name = os.getenv('GCS_BUCKET_NAME')
    credentials_path = os.getenv('GCS_CREDENTIALS_PATH', './gcs_storage_key.json')
    signed_urls_file = os.getenv('SIGNED_URLS_FILE', 'signed_urls.json')
    
    if not bucket_name:
        sys.exit("Error: GCS_BUCKET_NAME environment variable is required")
    if not os.path.exists(credentials_path):
        sys.exit(f"Error: Credentials file not found at {credentials_path}")
        
    return bucket_name, credentials_path, signed_urls_file

def list_bucket_files(bucket):
    """List all files in the bucket, excluding folder markers."""
    files = []
    try:
        blobs = bucket.list_blobs()
        for blob in blobs:
            # Skip folder markers (objects ending with '/')
            if not blob.name.endswith('/'):
                files.append(blob.name)
        return sorted(files)  # Sort files for consistent display
    except Exception as e:
        sys.exit(f"Error listing bucket contents: {e}")

def generate_signed_url(blob):
    """Generate a signed URL valid for 7 days."""
    try:
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=7),
            method="GET"
        )
        return url
    except Exception as e:
        sys.exit(f"Error generating signed URL: {e}")

def main():
    # Load configuration
    bucket_name, credentials_path, signed_urls_file = load_config()
    
    # Initialize GCS client
    try:
        client = storage.Client.from_service_account_json(credentials_path)
        bucket = client.bucket(bucket_name)
    except Exception as e:
        sys.exit(f"Error initializing GCS client: {e}")
    
    # List files
    files = list_bucket_files(bucket)
    
    if not files:
        sys.exit("No files found in bucket")
    
    # Display files with numbers
    print("\nFiles in bucket:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}) {file}")
    
    # Get user selection
    while True:
        choice = input("\nEnter the number of the file to sign (or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            sys.exit(0)
        
        try:
            file_idx = int(choice) - 1
            if 0 <= file_idx < len(files):
                selected_file = files[file_idx]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")
    
    # Generate signed URL
    blob = bucket.blob(selected_file)
    signed_url = generate_signed_url(blob)
    
    # Output results
    print(f"\nSigned URL for {selected_file} (valid for 7 days):")
    print(signed_url)
    
    # Try to copy to clipboard
    try:
        pyperclip.copy(signed_url)
        print("\nURL copied to clipboard!")
    except Exception:
        print("\nCould not copy to clipboard. Please copy the URL manually.")

if __name__ == "__main__":
    main() 