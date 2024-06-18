import os
import time
import json
import dotenv
import streamlit as st
from openai import OpenAI
from chat_with_assistant import chat_with_assistant

dotenv.load_dotenv()

# Initialize API client
api_key = os.getenv("OPEN_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=api_key)


st.set_page_config(page_title="DuckDuckGo Search Assistant", layout="wide")
st.title("DuckDuckGo Search Assistant")
st.markdown("Enter your search query below and get results from DuckDuckGo!")

user_query = st.text_input("Search Query")

if st.button("Search"):
    if user_query:
        with st.spinner("Fetching results..."):
            result = chat_with_assistant(user_query)
        st.markdown("## Search Results Please wait...!!!")
        st.write(result)
    else:
        st.warning("Please enter a search query.")
