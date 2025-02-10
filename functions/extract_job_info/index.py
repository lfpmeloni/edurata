import openai
import json

def handler(inputs):
    OPENAI_API_KEY = inputs.get("openai_api_key")  # Get API Key from inputs
    if not OPENAI_API_KEY:
        return {"error": "OPENAI_API_KEY is missing. Ensure it's set in Edurata Secrets."}

    job_description = inputs.get("job_description")
    if not job_description:
        return {"error": "Job description is missing."}

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

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Correct API usage
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )

        # Extract the response content
        completion = response.choices[0].message.content.strip()
        return {"job_info": completion}
    
    except Exception as e:
        return {"error": f"Error extracting job info: {str(e)}"}