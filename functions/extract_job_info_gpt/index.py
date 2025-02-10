import os
import openai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def handler(inputs):
    job_description = inputs.get("job_description", "")

    prompt = f"""
    You are an AI agent designed to extract key details from job descriptions...
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

        return json.loads(response['choices'][0]['message']['content'])

    except Exception as e:
        return {"error": f"Error extracting job info from GPT: {e}"}
