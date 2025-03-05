import requests
import yaml

def handler(inputs):
    github_repo_url = inputs.get("github_repo_url")
    workflow_path = inputs.get("workflow_path")

    if not github_repo_url or not workflow_path:
        return {"error": "Missing GitHub repository URL or workflow path."}

    # Convert GitHub URL to RAW content link
    raw_url = github_repo_url.replace("github.com", "raw.githubusercontent.com").replace("/tree/", "/") + f"/{workflow_path}"

    try:
        # Fetch the raw YAML content
        response = requests.get(raw_url)
        if response.status_code != 200:
            return {"error": f"Failed to fetch workflow YAML. Status Code: {response.status_code}"}

        yaml_content = response.text

        # Parse YAML to extract workflow details
        try:
            parsed_yaml = yaml.safe_load(yaml_content)
            workflow_details = {
                "name": parsed_yaml.get("name", "Unknown Workflow"),
                "description": parsed_yaml.get("description", "No description available."),
                "steps": parsed_yaml.get("steps", {})
            }
        except yaml.YAMLError:
            return {"error": "Invalid YAML format"}

        return {
            "yaml_content": yaml_content,
            "workflow_details": workflow_details
        }

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
