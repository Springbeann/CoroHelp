import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests

# Set your OpenAI API key
# openai.api_key = 'YOUR_API_KEY'  # This line is no longer needed since we'll be using user-provided API keys

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

def get_gpt_summary(content, api_key):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please summarize the following content:\n\n{content}"}
    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response.choices[0].message['content'].strip()

# Fetch content from predefined URLs in the background
combined_content = "\n\n---\n\n".join([fetch_content(url) for url in URLS])

# Streamlit UI
st.title("CoroHelp")
st.subheader("Your best assistant :orange[ever] :tangerine:")

# Input for OpenAI API Key
api_key = st.text_input("Enter your OpenAI API key:", type='password')

if api_key:
    # Input for user question
    user_question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        if not user_question:
            st.warning("Please enter a question.")
        else:
            answer = get_gpt_summary(user_question, api_key)
            st.write(answer)
else:
    st.warning("Please provide an OpenAI API key to proceed.")
