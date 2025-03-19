import os
import yaml

def handler(inputs):
    repo_dir = inputs.get("repoCode")
    workflow_path = inputs.get("workflowPath")

    if not repo_dir or not workflow_path:
        return {"error": "Missing repoCode or workflowPath input."}

    full_path = os.path.join(repo_dir, workflow_path)

    print(f"Checking for file at: {full_path}")

    if not os.path.exists(full_path):
        return {"error": f"File not found: {full_path}"}

    try:
        with open(full_path, 'r') as file:
            yaml_content = file.read()
            parsed_yaml = yaml.safe_load(yaml_content)

        return {"workflow_content": yaml_content}

    except yaml.YAMLError as e:
        return {"error": f"Failed to parse YAML: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
