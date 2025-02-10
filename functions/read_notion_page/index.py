import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# Initialize the Notion Client
notion = Client(auth=NOTION_API_KEY)

def handler(inputs):
    page_id = inputs.get("page_id")

    try:
        blocks = notion.blocks.children.list(block_id=page_id).get('results', [])
        content = ""

        for block in blocks:
            block_type = block.get('type')
            block_data = block.get(block_type, {})

            if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3']:
                text_elements = block_data.get('rich_text', [])
                text = "".join([part['plain_text'] for part in text_elements])
                content += text + " "

        return {"job_description": content.strip()}

    except Exception as e:
        return {"error": f"Error fetching Notion page {page_id}: {str(e)}"}
