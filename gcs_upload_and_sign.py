#!/usr/bin/env python3

import os
import re
import sys
import pyperclip
from datetime import timedelta
from pathlib import Path
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

def upload_and_sign(file_path, bucket_name, credentials_path):
    """
    Upload a file to GCS bucket and generate a signed URL
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
    
    # Upload the file
    blob = bucket.blob(sanitized_filename)
    blob.upload_from_filename(file_path)
    
    print(f"File uploaded as: {sanitized_filename}")
    
    # Generate signed URL (7 days is the maximum allowed time)
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(days=7),
        method="GET"
    )
    
    return signed_url

def main():
    if len(sys.argv) != 2:
        print("Usage: python upload_and_sign.py <file_path>")
        sys.exit(1)
    
    # Get configuration from environment variables with defaults
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
    
    try:
        signed_url = upload_and_sign(file_path, bucket_name, credentials_path)
        print("\nUpload successful!")
        print(f"Signed URL (valid for 7 days):\n{signed_url}")
        
        # Copy URL to clipboard
        pyperclip.copy(signed_url)
        print("\nURL has been copied to clipboard!")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 