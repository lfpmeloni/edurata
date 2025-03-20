import sys
import subprocess

# Ensure dependencies are installed
try:
    import requests
    import yaml
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "PyYAML"])
    import requests
    import yaml

def handler(inputs):
    github_repo_url = inputs.get("github_repo_url")
    workflow_path = inputs.get("workflow_path")
    record_id = inputs.get("record_id")  # Retrieve record_id from input

    if not github_repo_url or not workflow_path:
        return {"error": "Missing GitHub repository URL or workflow path."}

    try:
        # Extract repository owner and name
        parts = github_repo_url.rstrip("/").split("/")
        repo_owner = parts[-2]
        repo_name = parts[-1].replace(".git", "")
        branch = "main"

        # Construct the raw GitHub URL
        raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{workflow_path}"
    except Exception as e:
        return {"error": f"Failed to construct raw URL: {str(e)}"}

    print(f"🔍 Fetching YAML from: {raw_url}")

    try:
        response = requests.get(raw_url)

        if response.status_code != 200:
            print(f"⚠️ GitHub returned status {response.status_code}: {response.text}")
            return {"error": f"Failed to fetch workflow YAML. Status Code: {response.status_code}"}

        yaml_content = response.text

        try:
            parsed_yaml = yaml.safe_load(yaml_content)
            workflow_details = {
                "name": parsed_yaml.get("name", "Unknown Workflow"),
                "description": parsed_yaml.get("description", "No description available."),
                "steps": parsed_yaml.get("steps", {})
            }
        except yaml.YAMLError as e:
            print(f"❌ YAML Parsing Error: {str(e)}")
            return {"error": "Invalid YAML format"}

        return {
            "yaml_content": yaml_content,
            "workflow_details": workflow_details,
            "record_id": record_id  # Return record_id to next step
        }

    except Exception as e:
        print(f"🚨 Unexpected Error: {str(e)}")
        return {"error": f"Unexpected Error: {str(e)}"}
