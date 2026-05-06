import json
import os
from datetime import datetime, timezone
from urllib import request
from functools import cached_property
import hmac
import hashlib


class ResumeSubmitter:
    def __init__(self):
        self.submission_url = os.getenv("SUBMISSION_URL")
        self.repo_name = os.getenv("REPO_NAME")
        self.action_run_link = os.getenv("ACTION_RUN_LINK")
        self.signing_secret = os.getenv("SIGNING_SECRET")

        if not all(
            [
                self.repo_name,
                self.action_run_link,
                self.submission_url,
                self.signing_secret,
            ]
        ):
            raise ValueError(
                "Ensure to set REPO_NAME, ACTION_RUN_LINK, SUBMISSION_URL, and SIGNING_SECRET are set inside the environment."
            )

    @cached_property
    def payload(self):
        return json.dumps(
            {
                "timestamp": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
                "name": "Tapiwa Lason Mapfundematsva",
                "email": "tapiwa@tapiwa.io",
                "repository_link": "https://github.com/" + self.repo_name,
                "resume_link": "https://www.linkedin.com/in/tapiwa-lason/",
                "action_run_link": self.action_run_link,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    @cached_property
    def headers(self):
        signature = hmac.new(
            self.signing_secret.encode("utf-8"),
            self.payload,
            hashlib.sha256,
        ).hexdigest()
        return {
            "Content-Type": "application/json",
            "X-Signature-256": signature,
        }

    def submit(self):
        req = request.Request(
            self.submission_url,
            data=self.payload,
            headers=self.headers,
            method="POST",
        )

        try:
            with request.urlopen(req) as response:
                response_body = response.read().decode("utf-8")
                print("Status Code:", response.status)
                print("Response:", response_body)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    submitter = ResumeSubmitter()
    submitter.submit()
