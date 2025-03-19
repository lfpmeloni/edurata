import os
import yaml

def handler(inputs):
    repo_dir = inputs.get("repoCode")
    workflow_path = inputs.get("workflowPath")

    if not repo_dir or not workflow_path:
        return {"error": "Missing repoCode or workflowPath input."}

    # Ensure correct file path (avoid double path joining)
    full_path = os.path.normpath(os.path.join(repo_dir, workflow_path))

    # Debugging: List all files inside the repo before checking for the file
    print(f"📂 Repo directory structure of {repo_dir}:")
    for root, dirs, files in os.walk(repo_dir):
        level = root.replace(repo_dir, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}📄 {file}")

    print(f"\n🔍 Checking for file at: {full_path}")

    # Verify if the expected file exists
    if not os.path.exists(full_path):
        return {"error": f"⚠️ File not found: {full_path}"}

    try:
        with open(full_path, 'r') as file:
            yaml_content = file.read()
            parsed_yaml = yaml.safe_load(yaml_content)

        return {"workflow_content": yaml_content}

    except yaml.YAMLError as e:
        return {"error": f"Failed to parse YAML: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
