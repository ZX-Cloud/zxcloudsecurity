"""
trigger_workflow/lambda_function.py
Triggers a GitHub Actions workflow via the GitHub API.
Invoked by EventBridge Scheduler. Pass {"workflow_file": "<name>.yml"} in the
event to target a specific workflow; defaults to the daily pipeline for
backward compatibility with the existing 6am UTC schedule.
"""

import json
import boto3
import urllib.request
import urllib.error

GITHUB_OWNER = "ZX-Cloud"
GITHUB_REPO = "zxcloudsecurity"
DEFAULT_WORKFLOW_FILE = "daily-pipeline.yml"
SECRET_NAME = "zxcloudsecurity/github-token"
REGION = "eu-west-2"


def get_github_token() -> str:
    client = boto3.client("secretsmanager", region_name=REGION)
    response = client.get_secret_value(SecretId=SECRET_NAME)
    return response["SecretString"]


def handler(event, context):
    workflow_file = (event or {}).get("workflow_file", DEFAULT_WORKFLOW_FILE)
    print(f"Triggering GitHub Actions workflow: {workflow_file}")

    token = get_github_token()

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/{workflow_file}/dispatches"

    payload = json.dumps({"ref": "main"}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            print(f"GitHub API response: {status}")
            if status == 204:
                print("✅ Workflow triggered successfully")
                return {"statusCode": 200, "body": "Workflow triggered"}
            else:
                print(f"Unexpected status: {status}")
                return {"statusCode": status, "body": f"Unexpected status: {status}"}

    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ GitHub API error {e.code}: {body}")
        return {"statusCode": e.code, "body": body}

    except Exception as e:
        print(f"❌ Error: {e}")
        raise
