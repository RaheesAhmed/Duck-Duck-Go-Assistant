from openai import OpenAI
import os
import dotenv


dotenv.load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

client = OpenAI(api_key=api_key)

my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    instructions="You are a personal assistant that can perform web searches..",
    model="gpt-4o",
    name="Web Search Assistant",
    tools=[
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                "name": "get_text_results",
                "description": "Search DuckDuckGo for text information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query string.",
                        }
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_images_results",
                "description": "Search DuckDuckGo for images",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query string.",
                        }
                    },
                    "required": ["query"],
                },
            },
        },
    ],
)

print(my_updated_assistant)
print("Assistant updated successfully!")
