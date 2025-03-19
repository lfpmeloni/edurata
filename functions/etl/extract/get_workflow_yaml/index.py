import os
import yaml

def handler(inputs):
    repo_path = inputs.get("repoCode")

    if not repo_path:
        return {"error": "Missing repoCode input."}

    # Debugging: Print all files inside the cloned repository
    print(f"📂 Checking files in: {repo_path}")

    all_files = []
    for root, dirs, files in os.walk(repo_path):
        all_files.extend([os.path.join(root, file) for file in files])

    print("🗂️ Found files:")
    for file in all_files:
        print(f"  📄 {file}")

    # Verify if the expected workflow file exists
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
