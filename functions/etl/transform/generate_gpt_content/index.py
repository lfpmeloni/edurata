import openai
import os

def handler(inputs):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    raw_content = inputs["raw_content"]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI that generates professional blog posts from raw content."},
            {"role": "user", "content": f"Generate a well-structured, engaging blog post from this content:\n\n{raw_content}"}
        ],
        temperature=0.7
    )
    
    return {"generated_content": response["choices"][0]["message"]["content"]}