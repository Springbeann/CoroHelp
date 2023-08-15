import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests
from transformers import BartForConditionalGeneration, BartTokenizer

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

URLS = [
    "https://www.fona.com/articles/2017/09/a-global-look-at-juice",
    "https://www.globenewswire.com/en/news-release/2023/06/05/2681725/28124/en/Industrial-Sugar-Global-Market-Report-2023-Rise-in-Global-Consumption-of-Sugar-and-Growth-in-International-Trade-Boosts-Sector.html",     
    "https://www.trackmind.com/top-three-global-flavor-beverage-trends-for-2023/"
]

def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()[:1000000]

def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def get_gpt_answer(user_question, summarized_content, api_key):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Based on the following summarized content, answer the question: '{user_question}'\n\n{summarized_content}..."}
    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response.choices[0].message['content'].strip()

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
            answers = []
            for url in URLS:
                content = fetch_content(url)
                summarized_content = summarize_text(content)
                answer = get_gpt_answer(user_question, summarized_content, api_key)
                answers.append(answer)
            
            for idx, answer in enumerate(answers, 1):
                st.write(f"Answer based on URL {idx}: {answer}")
else:
    st.warning("Please provide an OpenAI API key to proceed.")


