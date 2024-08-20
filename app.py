import streamlit as st
import google.generativeai as geneai
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")

# Configure the geneai model with your API key
geneai.configure(api_key=api_key)
model = geneai.GenerativeModel('gemini-pro')

# Function to fetch top news using serp_api_key
def fetch_top_news():
    url = "https://newsapi.org/v2/top-headlines"
    headers = {
        "Authorization": f"Bearer {serp_api_key}",
    }
    params = {
        "language": "en",
        "pageSize": 5,
        "apiKey": serp_api_key
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        st.error("Failed to fetch top news.")
        return []

# Function to generate short summaries using the Gemini Pro model
def generate_short_summaries(news_articles):
    summaries = []
    for article in news_articles:
        title = article.get("title", "")
        content = article.get("content", "")
        
        if not title and not content:
            continue
        
        prompt = f"Generate a short summary for this news article: {title}. {content}"

        try:
            response = model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                summaries.append(response.text.strip())
            else:
                continue  # Skip the article if summary can't be generated
        except ValueError as e:
            st.error(f"Error generating summary: {e}")
            continue  # Skip the article if there's an error
    
    return summaries

# Streamlit app setup
st.set_page_config(page_title="Top News Summarizer", page_icon=":newspaper:", layout="wide")
st.title("Top News Summarizer")

st.markdown("""
**Welcome to the Top News Summarizer!**  
Fetch the latest top news from Google and get concise summaries powered by AI.
""")

# Button to fetch and summarize news
if st.button("Get Latest News Summaries"):
    with st.spinner("Fetching the latest top news..."):
        news_articles = fetch_top_news()
    
    if news_articles:
        with st.spinner("Generating summaries..."):
            summaries = generate_short_summaries(news_articles)
        
        if summaries:
            for i, summary in enumerate(summaries):
                st.subheader(f"News {i+1}: {news_articles[i]['title']}")
                st.write(summary)
                st.write(f"[Read more]({news_articles[i]['url']})")
                st.write("---")
        else:
            st.warning("No summaries could be generated.")
    else:
        st.error("No news articles found.")

# Footer
st.markdown("""
---
**Powered by [GeneAI](https://example.com) and serp_api_key**  
_Crafted with :heart: using Streamlit by Ajeetkumar Ukande_
""")
