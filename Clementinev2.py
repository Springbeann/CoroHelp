import streamlit as st
import openai
from googleapiclient.discovery import build

# Read the content of BeverageInsights.txt
with open("BeverageInsights.txt", "r") as file:
    content = file.read()

def google_search(query, api_key, cse_id):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id).execute()
    return res['items']

def get_gpt_response(user_question, content, api_key):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{user_question}\n\n{content}"}
    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response.choices[0].message['content'].strip()

# Streamlit UI
st.title(":orange[Clementine]")
st.subheader("Your favorite marketing :orange[assistant] :tangerine:")

# Input for OpenAI API Key
openai_api_key = st.text_input("Enter your OpenAI API key:", type='password')

# Sidebar for Google Search
st.sidebar.header("Google Search")
google_api_key = st.sidebar.text_input("Enter your Google API key:", type='password')
cse_id = "03d55e1bef04b46ef"  # Replace with your actual CSE ID
google_query = st.sidebar.text_input("Enter your Google search query:")
if st.sidebar.button("Search Google"):
    search_results = google_search(google_query, google_api_key, cse_id)
    search_content = "\n".join([result['snippet'] for result in search_results])
    st.sidebar.text_area("Search Results:", search_content)
    
    # Summarize the Google search results using GPT-3
    summary_question = "Provide a summary of the following search results:"
    summary = get_gpt_response(summary_question, search_content, openai_api_key)
    st.write("Summary of Google Search Results:")
    st.write(summary)

if openai_api_key:
    # Input for user question
    user_question = st.text_input("Enter your question based on the BeverageInsights report:")
    if st.button("Get Answer"):
        if not user_question:
            st.warning("Please enter a question.")
        else:
            answer = get_gpt_response(user_question, content, openai_api_key)
            st.write(answer)
else:
    st.warning("Please provide the OpenAI API key to proceed.")

