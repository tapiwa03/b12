import json
import os
from datetime import datetime, timezone
from urllib import request


submission_url = os.getenv("SUBMISSION_URL")
repo_name = os.getenv("REPO_NAME")
action_run_link = os.getenv("ACTION_RUN_LINK")


if all(
    [
        repo_name,
        action_run_link,
        submission_url,
    ]
):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "name": "Tapiwa Lason Mapfundematsva",
        "email": "tapiwa@tapiwa.io",
        "repository_link": "https://github.com/" + os.getenv("REPO_NAME"),
        "resume_link": "https://www.linkedin.com/in/tapiwa-lason/",
        "action_run_link": action_run_link,
    }

    data = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    req = request.Request(
        submission_url,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            print("Status Code:", response.status)
            print("Response:", response_body)
    except Exception as e:
        print("Error:", e)


else:
    print(
        "Ensure to set REPO_NAME, ACTION_RUN_LINK, and SUBMISSION_URL are set inside the environment."
    )
