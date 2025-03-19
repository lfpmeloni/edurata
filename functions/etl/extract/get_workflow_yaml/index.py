import os
import yaml

def handler(inputs):
    repo_path = inputs.get("repoCode")

    if not repo_path:
        return {"error": "Missing repoCode input."}

    print(f"📂 Checking for file at: {repo_path}")

    # Debug: List all files in the repo before checking
    for root, dirs, files in os.walk(os.path.dirname(repo_path)):
        print(f"📁 {root}/")
        for file in files:
            print(f"  📄 {file}")

    # Check if the file exists
    if not os.path.exists(repo_path):
        return {"error": f"⚠️ File not found: {repo_path}"}

    try:
        with open(repo_path, 'r') as file:
            yaml_content = file.read()
            parsed_yaml = yaml.safe_load(yaml_content)

        return {"workflow_content": yaml_content}

    except yaml.YAMLError as e:
        return {"error": f"Failed to parse YAML: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
