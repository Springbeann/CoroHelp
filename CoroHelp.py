import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests

# Set your OpenAI API key
openai.api_key = "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"

# Predefined URLs
URLS = [
    "https://lionelhitchen.com/the-rise-of-gen-z-flavours/",
    "https://www.foodbeverageinsider.com/market-trends-analysis/balancing-nutrition-and-appeal-childrens-food-and-beverage",
    "https://wellmune.com/2019/05/29/top-insights-for-childrens-beverage-market/" 
    "https://www.austriajuice.com/news-blog/flavour-trends" 
    "https://intracen.org/news-and-events/news/what-are-the-worlds-favourite-fruits"    
    "https://menuprice.co/blog/top-11-worlds-favorite-fruit-juices" 
    "https://eng.alimentossas.com/blog/fruit-flavors-which-are-the-most-popular-in-food-production" 
    "https://eng.alimentossas.com/blog/beverages/soft-drinks"   
    "https://foodinsight.org/spotlight-generation-z/"
]

def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def get_gpt_response(user_question, combined_content):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Based on the content from multiple webpages, answer the question: '{user_question}'\n\n{combined_content[:2000]}..."}  # Using only the first 2000 characters for brevity
    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response.choices[0].message['content'].strip()

# Fetch content from predefined URLs in the background
combined_content = "\n\n---\n\n".join([fetch_content(url) for url in URLS])

# Streamlit UI
st.title("GPT-3 Web Content Assistant")

# Input for user question
user_question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not user_question:
        st.warning("Please enter a question.")
    else:
        answer = get_gpt_response(user_question, combined_content)
        st.write(answer)  

