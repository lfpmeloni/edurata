import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")

def handler(inputs):
    database_id = inputs.get("notion_database_id")
    
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Company Name": {"title": [{"text": {"content": inputs.get("Company Name", "Unknown")}}]},
            "Status": {"status": {"name": "Not applied"}},
            "Date": {"date": {"start": inputs.get("iso_time")}},
            "Job Name": {"rich_text": [{"text": {"content": inputs.get("Job Name", "Unknown")}}]},
            "Job Description": {"rich_text": [{"text": {"content": inputs.get("Short Job Description", "")}}]}
        }
    }

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.notion.com/v1/pages", json=data, headers=headers)
    
    return response.json()