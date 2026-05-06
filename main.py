import json
import os
from datetime import datetime, timezone
from urllib import request
from functools import cached_property
import hmac
import hashlib


class ResumeSubmitter:
    def __init__(self):
        REQUIRED_ENV_VARS = [
            "REPO_NAME",
            "ACTION_RUN_LINK",
            "NAME",
            "EMAIL",
            "RESUME_LINK",
            "SUBMISSION_URL",
            "SIGNING_SECRET",
        ]

        env = {var: os.getenv(var) for var in REQUIRED_ENV_VARS}
        missing = [k for k, v in env.items() if not v]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        self.repo_name = env["REPO_NAME"]
        self.action_run_link = env["ACTION_RUN_LINK"]
        self.name = env["NAME"]
        self.email = env["EMAIL"]
        self.resume_link = env["RESUME_LINK"]
        self.submission_url = env["SUBMISSION_URL"]
        self.signing_secret = env["SIGNING_SECRET"]

    @cached_property
    def payload(self):
        return json.dumps(
            {
                "timestamp": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
                "name": self.name,
                "email": self.email,
                "repository_link": "https://github.com/" + self.repo_name,
                "resume_link": self.resume_link,
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
            "X-Signature-256": f"sha256={signature}",
        }

    def submit(self):
        req = request.Request(
            self.submission_url,
            data=self.payload,
            headers=self.headers,
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=10) as response:
                response_body = response.read().decode("utf-8")
                print("Status Code:", response.status)

                receipt = json.loads(response_body).get("receipt")
                if not receipt:
                    raise ValueError("No receipt found in the response.")
                print("Receipt: ", receipt)

        except Exception as e:
            print("Error:", e)
            exit(1)


if __name__ == "__main__":
    submitter = ResumeSubmitter()
    submitter.submit()
