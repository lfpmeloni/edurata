import openai

def handler(inputs):
    # Fetch API key from inputs
    api_key = inputs.get("openai_api_key")
    if not api_key:
        return {"error": "OPENAI_API_KEY is missing. Ensure it's set in Edurata Secrets."}

    # Fetch raw content
    raw_content = inputs.get("raw_content")
    if not raw_content:
        return {"error": "raw_content is missing."}

    try:
        # Call OpenAI API
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates professional blog posts from raw content."},
                {"role": "user", "content": f"Generate a well-structured, engaging blog post from this content:\n\n{raw_content}"}
            ],
            temperature=0.7
        )

        return {"generated_content": response["choices"][0]["message"]["content"]}

    except openai.error.OpenAIError as e:
        return {"error": f"OpenAI API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
