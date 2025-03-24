# Google Cloud Storage URL Generator

This tool provides scripts for uploading files to Google Cloud Storage and generating signed URLs, with additional features for tracking URL expiration.

## Features

- Upload files to Google Cloud Storage
- Generate signed URLs (valid for 7 days)
- Automatic clipboard copy of generated URLs
- Track URL expiration dates
- Clean up and monitor expired URLs

## Requirements

- Python 3.x
- Google Cloud Storage account and credentials
- Required Python packages (install via `pip install -r requirements.txt`):
  - google-cloud-storage
  - python-dotenv
  - pyperclip

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.template` to `.env` and configure:
   ```bash
   cp .env.template .env
   ```
4. Edit `.env` file with your settings:
   ```
   GCS_BUCKET_NAME=your-bucket-name
   GCS_CREDENTIALS_PATH=./gcs_storage_key.json
   ```
5. Place your Google Cloud Storage credentials JSON file in the project directory

## Usage

### Upload and Generate Signed URL

```bash
python gcs_upload_and_sign.py <file_path>
```

This will:
- Upload the file to GCS
- Generate a signed URL (valid for 7 days)
- Copy the URL to clipboard
- Store URL information for tracking

### Check Expired URLs

```bash
python check_expired_urls.py
```

This will:
- Show all valid URLs with remaining days
- Remove expired URLs from tracking
- Display a report of valid and expired URLs

### Manage Stored URLs

```bash
python manage_urls.py
```

This will:
- Display all stored URLs with their status
- Allow you to delete specific URLs
- Clean up expired URLs
- Manage all URL records interactively

## URL Tracking

URLs are tracked in `signed_urls.json` with the following information:
- Original signed URL
- Creation timestamp
- Expiration date
- Filename

## Notes

- Signed URLs are valid for 7 days (maximum allowed by Google Cloud Storage)
- Filenames are automatically sanitized (lowercase, no special characters)
- URLs are automatically copied to clipboard after generation

## Troubleshooting

- If clipboard copying fails, ensure you have proper permissions and a display server running
- For Linux users, you might need to install `xclip` or `xsel`:
  ```bash
  # For Debian/Ubuntu
  sudo apt-get install xclip
  # For Fedora
  sudo dnf install xclip
  ```

## License

[Add your license information here]

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

