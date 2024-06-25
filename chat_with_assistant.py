import os
import time
import json
import dotenv
from openai import OpenAI
from duck_duck_go import get_text_results, get_images_results
from scrape_url import scrape_url

dotenv.load_dotenv()

# Initialize API client
api_key = os.getenv("OPEN_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=api_key)


def upload_file(file_path):
    """Uploads a file and returns its ID."""
    with open(file_path, "rb") as file:
        uploaded_file = client.files.create(file=file, purpose="assistants")
    return uploaded_file.id


def chat_with_assistant(user_query, file_path=None, thread_id=None):
    try:

        # Upload file if path is provided
        file_id = upload_file(file_path) if file_path else None

        if thread_id is None:
            print("Creating new thread...")
            thread = client.beta.threads.create()

            thread_id = thread.id
            print(f"New thread created with ID: {thread_id}")
        else:
            print(f"Using existing thread ID: {thread_id}")

        # Prepare message attachments if file is uploaded
        attachments = (
            [{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
            if file_id
            else []
        )

        print("Adding user message to thread...")
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"""{user_query} """,
            attachments=attachments,
        )
        print(f"User message added with ID: {message.id}")

        # Create and poll the run
        print("Creating and polling the run...")
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        print(f"Run created with status: {run.status}")

        while run.status == "requires_action":
            tool_outputs = []
            print("Run requires action. Processing tool calls...")

            if run.required_action and run.required_action.submit_tool_outputs:
                for tool in run.required_action.submit_tool_outputs.tool_calls:
                    print(f"Processing tool call for function: {tool.function.name}")

                    if tool.function.name == "get_text_results":
                        query = json.loads(tool.function.arguments)["query"]
                        data = get_text_results(query)
                        tool_outputs.append(
                            {"tool_call_id": tool.id, "output": json.dumps(data)}
                        )
                    elif tool.function.name == "get_images_results":
                        query = json.loads(tool.function.arguments)["query"]
                        images = get_images_results(query)
                        tool_outputs.append(
                            {"tool_call_id": tool.id, "output": json.dumps(images)}
                        )
                    elif tool.function.name == "scrape_url":
                        url = json.loads(tool.function.arguments)["url"]
                        content = scrape_url(url)
                        tool_outputs.append(
                            {"tool_call_id": tool.id, "output": json.dumps(content)}
                        )

                # Submit the tool outputs if there are any
                if tool_outputs:
                    print("Submitting tool outputs...")
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                else:
                    print("No tool outputs to submit.")
            else:
                print("No required action found or no tool calls.")

            # Retrieve the run status again
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(f"Current run status: {run.status}")

        # Poll for the final status of the run until completion
        while run.status not in ["completed", "failed"]:
            print("Run not completed. Polling again...")
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(f"Current run status: {run.status}")

        # Check the final status of the run
        if run.status == "completed":
            print("Run completed. Fetching messages...")
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            for message in messages.data:
                print(message.content[0].text.value)
                return message.content[0].text.value
        else:
            print(f"Run ended with status: {run.status}")
            return "An error occurred. Please try again later."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An internal error occurred. Please try again later."


# Example usage
# user_query = "search the openai updates"
# chat_with_assistant(user_query)
