import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests
from transformers import BartForConditionalGeneration, BartTokenizer


model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

URLS = [
    "https://menuprice.co/blog/top-11-worlds-favorite-fruit-juices",
    "https://intracen.org/news-and-events/news/what-are-the-worlds-favourite-fruits",     
    "https://foodinsight.org/spotlight-generation-z/"

]
@st.cache_data
def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()[:100000]

def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def get_gpt_summary(user_question, webpage_content, api_key):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Based on the following webpage content, answer the question: '{user_question}'\n\n{webpage_content}..."}  

    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response.choices[0].message['content'].strip()

# Fetch content from predefined URLs in the background
combined_content = "\n\n---\n\n".join([summarize_text(fetch_content(url)) for url in URLS])

# Streamlit UI
st.title("Clementine")
st.subheader("Your favorite market research :orange[assistant] :tangerine:")

# Input for OpenAI API Key
api_key = st.text_input("Enter your OpenAI API key:", type='password')  

if api_key:
    # Input for user question
    user_question = st.text_input("Enter your question:")
    if st.button("Search our database"):
        if not user_question:
            st.warning("Please enter a question.")
        else:
            answer = get_gpt_summary(user_question, combined_content, api_key)  # Pass combined_content as the second argument
            st.write(answer)
else:
    st.warning("Please provide an OpenAI API key to proceed.")

