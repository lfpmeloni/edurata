import os
import datetime
import openai
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (Ensure these are set in Edurata secrets)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EDURATA_API_KEY = os.getenv("EDURATA_API_KEY")  # New API Key for Edurata

# Configure OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Define Edurata API endpoint for job cards
EDURATA_JOB_API_URL = "https://api.edurata.io/v1/jobs"

def extract_job_info_from_gpt(job_description):
    prompt = f"""
    You are an AI agent designed to extract key details from job descriptions. Based on the following job description, provide the information in JSON format with these fields:
    - "Company Name": string
    - "Job Name": string - Bring the complete name including field, if provided
    - "Language": string (e.g., "English, German") - If multiple languages, separate by comma
    - "Working Model": string (e.g., "Remote, Hybrid, Office") - If mentioned that hybrid or remote is possible, bring this possibility
    - "Location": string (e.g., city name where office is based, "Remote" is not applicable)
    - "Role": string (e.g., "Software Engineer", "Project Manager", "Developer")
    - "Short Job Description": string (1-2 sentences summary)
    - "Salary Expectation": number (salary expectation in euros per year, if unavailable make a guess based on seniority)

    Job Description:
    {job_description}

    Respond in JSON format only.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        return json.loads(response['choices'][0]['message']['content'])  # Return as JSON object
    except Exception as e:
        print(f"Error extracting job info from GPT: {e}")
        return None

def create_edurata_job_card(job_info):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Construct payload
    payload = {
        "company_name": job_info.get("Company Name", "Unknown"),
        "job_name": job_info.get("Job Name", "Unknown"),
        "status": "Not applied",
        "date": today_date,
        "short_description": job_info.get("Short Job Description", ""),
        "language": job_info.get("Language", "N/A"),
        "working_model": job_info.get("Working Model", "N/A"),
        "location": job_info.get("Location", "N/A"),
        "role": job_info.get("Role", "N/A"),
        "salary_expectation": job_info.get("Salary Expectation", 0),
    }

    headers = {
        "Authorization": f"Bearer {EDURATA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(EDURATA_JOB_API_URL, json=payload, headers=headers)
        if response.status_code == 201:
            print("Job card created successfully on Edurata.")
            return response.json()
        else:
            print(f"Failed to create job card: {response.text}")
            return None
    except Exception as e:
        print(f"Error creating job card on Edurata: {e}")
        return None

# Main function to execute workflow
def main(job_description):
    job_info = extract_job_info_from_gpt(job_description)
    if not job_info:
        print("Failed to retrieve job info.")
        return None

    return create_edurata_job_card(job_info)

# Example Usage
if __name__ == "__main__":
    example_description = "A software engineer is needed to work on backend development using Python and Django."
    print(main(example_description))
