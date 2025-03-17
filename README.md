# GCS File Uploader and URL Signer

This Python script allows you to upload files to Google Cloud Storage and generate signed URLs. The script automatically sanitizes filenames by converting them to lowercase and removing special characters.

## Prerequisites

1. Python 3.12 or later
2. A Google Cloud Service Account with appropriate permissions
3. The service account key file (`gcs_storage_key.json`)

## Setup

1. Install Python dependencies:
```sh
pip install -r requirements.txt
```

2. Create and configure your environment file:
```sh
# Copy the template file
cp .env.template .env

# Edit the .env file with your settings
vim .env
```

## Usage

Run the script with a file path as an argument:

```sh
python gcs_upload_and_sign.py "/path/to/your/file.pdf"
```

Note: The script will automatically load environment variables from the `.env` file.

### What the Script Does

1. Takes a file path as input
2. Sanitizes the filename:
   - Converts to lowercase
   - Removes special characters
   - Replaces spaces with underscores
3. Uploads the file to the GCS bucket
4. Generates a signed URL valid for 7 days (maximum allowed time)

### Example

```sh
# Upload a file with spaces and special characters
python gcs_upload_and_sign.py "My File (2024)!.pdf"
```

This will:
- Sanitize the filename to: `my_file_2024.pdf`
- Upload it to the bucket
- Generate and display a signed URL

### Output

The script will output:
- The sanitized filename used for upload
- The signed URL (valid for 7 days)
- Any error messages if something goes wrong

## Error Handling

The script includes checks for:
- Missing file path argument
- Missing environment variables
- Non-existent files or credentials
- Upload failures
- URL signing issues

## Configuration

The following settings are configured through environment variables:
- `GCS_BUCKET_NAME`: Your Google Cloud Storage bucket name (required)
- `GCS_CREDENTIALS_PATH`: Path to your service account key file (optional, defaults to ./gcs_storage_key.json)
- URL validity period: 7 days (fixed)

## Requirements

- google-cloud-storage>=2.14.0

## Notes

- The signed URL will expire after 7 days
- File names are automatically sanitized to ensure compatibility
- Original files are not modified; only the uploaded version has a sanitized name

## Initial Setup (if needed)

### Service Account Setup

1. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating) in your Google Cloud Project
2. [Grant the required permissions](https://cloud.google.com/storage/docs/access-control/iam-roles) to your service account:
   - `roles/storage.objectViewer` - for reading objects
   - `roles/storage.objectCreator` - for uploading objects
   - `roles/storage.signUrlMember` - for creating signed URLs

3. [Create and download the service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating):
```sh
source .env && gcloud --project=${PROJECT} iam service-accounts keys create gcs_storage_key.json \
  --iam-account gcs-signer@${PROJECT}.iam.gserviceaccount.com
```

⚠️ **Security Note**: 
- Keep your service account key secure and never commit it to version control
- Add `.env` and `gcs_storage_key.json` to your `.gitignore` file
- Consider using [Workload Identity](https://cloud.google.com/iam/docs/workload-identity-federation) for production environments

## Development Setup

### Python Version Management with pyenv

We recommend using [pyenv](https://github.com/pyenv/pyenv) to manage Python versions. Here's how to get started:

1. Install pyenv:
   - **macOS** (using Homebrew):
     ```bash
     brew install pyenv
     ```
   - **Linux**:
     ```bash
     curl https://pyenv.run | bash
     ```
   - For detailed installation instructions, visit the [pyenv installation guide](https://github.com/pyenv/pyenv#installation)

2. Add pyenv to your shell configuration:
   ```bash
   # For bash users (add to ~/.bashrc):
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc

   # For zsh users (add to ~/.zshrc):
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```
   
   After adding these lines, restart your shell or run:
   ```bash
   # For bash:
   source ~/.bashrc
   
   # For zsh:
   source ~/.zshrc
   ```

3. Install and set the Python version for this project:
   ```bash
   # install pyenv python version
   pyenv install 3.12

   # create virtualenv for the project
   pyenv virtualenv 3.12.6 gcs_upload_and_sign

   # set local virtualenv
   pyenv local gcs_upload_and_sign

   # install dependencies
   pip install -r requirements.txt
   ```
