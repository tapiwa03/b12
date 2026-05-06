# Resume Submission Tool

A Python utility for submitting resume information via a signed HTTP POST request.

## Features

-   **ISO 8601 Timestamps**: Uses UTC timestamps in ISO 8601 format with `Z` suffix
-   **HMAC-SHA256 Signing**: Signs request body with a secret key for verification
-   **Compact JSON**: Serializes payload with minimal whitespace and sorted keys
-   **Environment-Based Configuration**: All credentials and URLs sourced from environment variables

## How It Works

1. GitHub Actions triggers the script
2. The script constructs a canonical JSON payload
3. The payload is signed using HMAC-SHA256
4. A POST request is sent to the submission endpoint
5. The response receipt is printed in the workflow logs

## Environment Variables

Required environment variables:

-   `SUBMISSION_URL` — The endpoint URL where the resume is submitted
-   `REPO_NAME` — GitHub repository name. Is manually set in local dev but picked up from Github Actions when live
-   `ACTION_RUN_LINK` — Link to the GitHub Actions workflow run. Picked up in Github Actions but needs to be manually set for local dev
-   `SIGNING_SECRET` — Secret key used for HMAC-SHA256 signing
-   `NAME` - Name used for the application data
-   `EMAIL` - Email used for the application data
-   `RESUME_LINK` - A publicly available link to the desired resume

## Usage

Locally, just set environment variables and run this below

```shell
python main.py
```

> When running locally, you must manually set environment variables such as ACTION_RUN_LINK.

## GitHub Actions

The workflow automatically injects:

-   repository name
-   run link
-   secrets (name, email, resume)

Trigger it from the Actions tab → Run workflow.
