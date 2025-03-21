import openai

def handler(inputs):
    api_key = inputs.get("openai_api_key")
    raw_content = inputs.get("raw_content")
    messages = inputs.get("messages")
    model = inputs.get("model", "gpt-4")
    temperature = inputs.get("temperature", 0.7)

    if not api_key:
        return {"error": "OPENAI_API_KEY is missing."}
    if not raw_content:
        return {"error": "raw_content is missing."}
    if not messages:
        return {"error": "messages array is missing."}

    # Optional: used to carry metadata forward
    workflow_id = inputs.get("workflow_id")

    try:
        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        return {
            "generated_content": response.choices[0].message.content,
            "workflow_id": workflow_id  # Pass-through if provided
        }

    except openai.OpenAIError as e:
        return {"error": f"OpenAI API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
