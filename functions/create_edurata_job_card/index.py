import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Edurata API Endpoint
EDURATA_JOB_API_URL = "https://api.edurata.io/v1/jobs"

def handler(inputs):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Construct payload
    payload = {
        "company_name": inputs.get("Company Name", "Unknown"),
        "job_name": inputs.get("Job Name", "Unknown"),
        "status": "Not applied",
        "date": today_date,
        "short_description": inputs.get("Short Job Description", ""),
        "language": inputs.get("Language", "N/A"),
        "working_model": inputs.get("Working Model", "N/A"),
        "location": inputs.get("Location", "N/A"),
        "role": inputs.get("Role", "N/A"),
        "salary_expectation": inputs.get("Salary Expectation", 0),
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('EDURATA_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(EDURATA_JOB_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": f"Error creating job card on Edurata: {e}"}
