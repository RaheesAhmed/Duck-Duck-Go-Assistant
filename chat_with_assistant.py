import os
import time
import json
import dotenv
from openai import OpenAI
from duck_duck_go import get_text_results, get_images_results

dotenv.load_dotenv()

# Initialize API client
api_key = os.getenv("OPEN_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=api_key)


def chat_with_assistant(user_query):
    try:
        # Create a thread and add a user message
        print("Creating thread...")
        thread = client.beta.threads.create()
        print(f"Thread created with ID: {thread.id}")

        print("Adding user message to thread...")
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"""search about {user_query}""",
        )
        print(f"User message added with ID: {message.id}")

        # Create and poll the run
        print("Creating and polling the run...")
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
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

                # Submit the tool outputs if there are any
                if tool_outputs:
                    print("Submitting tool outputs...")
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                else:
                    print("No tool outputs to submit.")
            else:
                print("No required action found or no tool calls.")

            # Retrieve the run status again
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Current run status: {run.status}")

        # Poll for the final status of the run until completion
        while run.status not in ["completed", "failed"]:
            print("Run not completed. Polling again...")
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Current run status: {run.status}")

        # Check the final status of the run
        if run.status == "completed":
            print("Run completed. Fetching messages...")
            messages = client.beta.threads.messages.list(thread_id=thread.id)
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
# user_query = "search the apple updates"
# chat_with_assistant(user_query)
