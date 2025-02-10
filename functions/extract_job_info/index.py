import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def handler(inputs):
    job_description = inputs.get("job_description", "")

    prompt = f"""
    You are an AI that extracts job details. Provide JSON output with these keys:
    - "company_name"
    - "job_name"
    - "language"
    - "working_model"
    - "location"
    - "role"
    - "short_job_description"
    - "salary_expectation"

    Job Description:
    {job_description}

    Respond **only** in JSON.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    try:
        content = response['choices'][0]['message']['content']
        return json.loads(content)  # Ensure valid JSON response
    except Exception as e:
        return {"error": f"Failed to parse GPT response: {str(e)}"}
