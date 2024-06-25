import streamlit as st
import random
import time
from test import chat_with_assistant
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

# Initialize API client
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=api_key)

# UI Enhancements
st.set_page_config(page_title="Real Estate Assistant", page_icon="🏡", layout="wide")

st.title("🏡 Real Estate Assistant")
st.write(
    "Welcome to your Real Estate Assistant! Ask any questions about real estate, market trends, or property details. You can also upload files for analysis."
)

# Initialize chat history and thread ID
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept file upload
file = st.file_uploader("Upload a file")

# Accept user input
prompt = st.chat_input("Send message to assistant")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Handle file upload
    if file:
        with open(f"temp/{file.name}", "wb") as f:
            f.write(file.getbuffer())
        file_path = f"temp/{file.name}"
    else:
        file_path = None

    # Get assistant response
    with st.spinner("Processing..."):
        with st.chat_message("assistant"):
            if st.session_state.thread_id is None:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id
            else:
                thread = client.beta.threads.retrieve(st.session_state.thread_id)

            response = chat_with_assistant(
                prompt, file_path, st.session_state.thread_id
            )
            assistant_response = response
            st.markdown(assistant_response)

    # Add assistant response to chat history and update thread ID
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )
