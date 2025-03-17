import yaml
import os
import sys

def handler(inputs):
    print(f"Python Version: {sys.version}")  # Debugging
    print(f"Checking PyYAML: {yaml.__version__}")  # Debugging

    repo_path = inputs.get("repoCode")

    if not repo_path:
        return {"error": "Missing repoCode input."}

    if not os.path.exists(repo_path):
        return {"error": f"File not found: {repo_path}"}

    try:
        with open(repo_path, 'r') as file:
            yaml_content = file.read()
            parsed_yaml = yaml.safe_load(yaml_content)

        return {"workflow_content": yaml_content}

    except yaml.YAMLError as e:
        return {"error": f"Failed to parse YAML: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}