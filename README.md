# Google Cloud Storage URL Manager

A tool for managing Google Cloud Storage signed URLs with features for uploading, tracking, and managing URL expiration.

## Features

- Upload files to Google Cloud Storage with progress tracking
- Generate signed URLs (valid for 7 days)
- Automatic clipboard copy of generated URLs
- Track URL expiration dates and history
- Interactive URL management interface
- Support for multiple URLs per file (history tracking)
- Visual progress bar for file uploads
- Color-coded status indicators

## Requirements

- Python 3.x
- Google Cloud Storage account and credentials
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```
4. Configure your `.env` file:
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

### Manage URLs

```bash
python manage_urls.py
```

The management interface provides options to:
1. **Manage/Delete URLs**
   - Delete specific URLs
   - Remove all expired URLs
   - Delete all URLs
   - View URL history
2. **View Active URL**
   - Show URL details
   - Copy URL to clipboard
   - Check expiration status

### URL Information

URLs are tracked with:
- Current status (VALID/EXPIRED)
- Days remaining until expiration
- Creation timestamp
- History of previous URLs (up to 5)
- File association

## Features in Detail

### Upload Progress
- Visual progress bar showing:
  - Upload speed
  - Estimated time remaining
  - Percentage complete
  - File size

### URL Management
- Color-coded status indicators
  - Green: Valid URLs
  - Red: Expired URLs
- URL history tracking
- Bulk URL management
- Automatic clipboard integration

### File Handling
- Automatic file sanitization
- Secure upload process
- Progress tracking
- Checksum verification

## Notes

- Signed URLs are valid for 7 days (maximum allowed by Google Cloud Storage)
- Filenames are automatically sanitized (lowercase, no special characters)
- URLs are tracked in `signed_urls.json`
- Previous URLs are kept in history (up to 5 per file)

## Troubleshooting

### Clipboard Issues
- For Linux users, install xclip or xsel:
  ```bash
  # Debian/Ubuntu
  sudo apt-get install xclip
  # Fedora
  sudo dnf install xclip
  ```

### Common Issues
- If upload fails, check your credentials and bucket permissions
- If clipboard copying fails, ensure you have proper permissions
- For connection issues, verify your Google Cloud credentials

## Security Considerations

- Credentials are never logged or stored in URL history
- Environment variables are used for sensitive configuration
- Files are uploaded with secure defaults
- URLs are generated with proper expiration handling

## Contributing

[Add your contribution guidelines here]

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

