import os
import yaml

def handler(inputs):
    repo_path = inputs.get("repoCode")

    if not repo_path:
        return {"error": "Missing repoCode input."}

    # Debugging: Print all files inside the cloned repository
    print(f"📂 Checking files in repo: {repo_path}")

    all_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"  📄 {file_path}")
            all_files.append(file_path)

    if not all_files:
        return {"error": "⚠️ No files found in the cloned repository!"}

    return {"debug_files": all_files}  # Just returning files found for debug
