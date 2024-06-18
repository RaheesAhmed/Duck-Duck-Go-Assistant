from openai import OpenAI
import time
import os
import dotenv


dotenv.load_dotenv()

# commit the following lines if you are using the code in a Replit environment
api_key = os.getenv("OPEN_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

client = OpenAI(api_key=api_key)


def retreive_assistant():
    assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
    print(assistant)
    return assistant


retreive_assistant()
