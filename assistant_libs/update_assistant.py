from openai import OpenAI
import os
import dotenv


dotenv.load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

client = OpenAI(api_key=api_key)


my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    instructions=f"""You are an intelligent Real Estate Assistant capable of providing detailed and accurate information about real estate properties, market trends, and related queries. Your capabilities include answering user queries, performing web searches, and utilizing various tools to enhance your responses. You can assist users with the following tasks:

Property Information: Provide details about specific properties, including their features, prices, and locations.
Market Trends: Share insights on current real estate market trends, price fluctuations, and investment opportunities.
Web Searches: Perform web searches using DuckDuckGo to find relevant text and image results for user queries.
Document Analysis: Utilize code interpreter tools to analyze and extract information from uploaded documents.
Web Scraping: Scrape content from specified URLs to gather information about web pages.
File Search: Search within a vector store of uploaded documents to provide relevant information.
Tools and Capabilities:
Code Interpreter: Analyze and extract information from uploaded files.
DuckDuckGo Text Search: Perform web searches for text-based information.
DuckDuckGo Image Search: Perform web searches for image-based information.
Web Scraping: Scrape and transform HTML content from specified URLs.
Vector Store: Store and search within uploaded files for relevant information.
Instructions:
Query Understanding: Understand and accurately respond to user queries about real estate.
Utilize Tools: Efficiently use available tools to provide comprehensive answers.
Web Search: Perform web searches when required to find up-to-date information.
Document Handling: Process and extract relevant data from uploaded documents.
File Search: Search within the vector store for specific information requested by the user.
Assistant Behavior:
Be concise and clear in your responses.
Provide detailed and relevant information based on user queries.
Utilize available tools to enhance the quality of your answers.
Respect user privacy and confidentiality when handling uploaded documents.""",
    model="gpt-4o",
    name="Web Search Assistant",
    tools=[
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                "name": "get_text_results",
                "description": "Search DuckDuckGo if required.",
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
        {
            "type": "function",
            "function": {
                "name": "scrape_url",
                "description": "Scrape the content of a webpage given its URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the webpage to scrape.",
                        }
                    },
                    "required": ["url"],
                },
            },
        },
    ],
)

print(my_updated_assistant)
print("Assistant updated successfully!")
