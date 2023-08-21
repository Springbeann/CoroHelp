import streamlit as st
from googleapiclient.discovery import build

def google_search(query, api_key, cse_id):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id).execute()
    return res['items']

def get_gpt_response(user_question, api_key, past_messages, presets=None):
    import openai
    openai.api_key = api_key
    if presets:
        messages = presets + [{"role": "user", "content": f"{user_question}"}]
    else:
        messages = past_messages + [{"role": "user", "content": f"{user_question}"}]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message['content'].strip(), messages

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
    st.sidebar.text_area("Snippet:", search_content)
    
    # Summarize the Google search results using GPT-4
    summary_question = "Provide a summary of the following search results:"
    try:
        summary, _ = get_gpt_response(summary_question, openai_api_key, [{"role": "system", "content": "You are a helpful assistant."}], search_content)
        st.write("Summary of Google Search Results:")
        st.write(summary)
    except Exception as e:
        st.error(f"Error: {e}")

past_messages = [{"role": "system", "content": "You are a helpful assistant."}]
if openai_api_key:
    # Input for user question
    user_question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        if not user_question:
            st.warning("Please enter a question.")
        else:
            try:
                answer, past_messages = get_gpt_response(user_question, openai_api_key, past_messages)
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please provide the OpenAI API key to proceed.")
