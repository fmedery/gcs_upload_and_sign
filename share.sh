#!/bin/bash
set -e

PROJECT="files-sharing-only"
DURATION="7d"
CLOUDSDK_PYTHON_SITEPACKAGES=1
CLOUDSDK_PYTHON=/Users/fmedery/.pyenv/shims/python
bucket="gs://industrielle_alliance-sharing"

while [[ -z "$FILE" ]]; do
  read -r -p "Enter the value for file to share: " FILE
done

#copy $FILE to GCS
FULL_PATH="~/Downloads/$FILE"
gcloud --project=${PROJECT} storage cp $FULL_PATH gs://industrielle_alliance-sharing/

#sign url
gcloud --project=${PROJECT} storage sign-url ${bucket}/{FILE} \
  --private-key-file=./gcs_storage_key.json \
  --duration=${DURATION}

