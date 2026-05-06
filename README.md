# Resume Submission Tool

A Python utility for submitting resume information via a signed HTTP POST request.

## Features

-   **ISO 8601 Timestamps**: Uses UTC timestamps in ISO 8601 format with `Z` suffix
-   **HMAC-SHA256 Signing**: Signs request body with a secret key for verification
-   **Compact JSON**: Serializes payload with minimal whitespace and sorted keys
-   **Environment-Based Configuration**: All credentials and URLs sourced from environment variables

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

To run it, all thats needed is python 3.11 and above

```shell
python main.py
```

## Payload Structure

The submission includes:

-   `action_run_link` — GitHub Actions workflow run URL
-   `email` — Submitter email address
-   `name` — Submitter name
-   `repository_link` — GitHub repository URL
-   `resume_link` — LinkedIn profile URL
-   `timestamp` — ISO 8601 UTC timestamp

Keys are sorted alphabetically in the JSON output.

## Signature Header

The request includes an `X-Signature-256` header with format:

```
X-Signature-256: sha256={hex-digest}
```

The signature is computed over the exact UTF-8-encoded JSON bytes using the signing secret as the key.
