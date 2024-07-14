import streamlit as st
from newspaper import Article
import google.generativeai as genai
import os

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from the Gemini AI model
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

# Function to scrape content from the given URL using newspaper3k
def scrape_content(url):
    try:
        article = Article(url, language='en')  # Specify language for better parsing
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        st.error(f"Error fetching the content from the website: {e}")
        return None

# Streamlit app configuration
st.set_page_config(page_title="News Summarizer")
st.markdown("<h1 style='text-align: center;'>News Summarizer</h1>", unsafe_allow_html=True)
st.header("Summarize News Articles from News Paper")

# Input field for the news URL
url = st.text_input("Enter the URL of the news article", "")

# Button to trigger summarization
summarize_news = st.button("Summarize News")

# If the button is pressed, scrape the content and generate the summary
if summarize_news:
    if url:
        st.write("Fetching content from the website...")
        content = scrape_content(url)
        
        if content:
            st.write("Generating summary...")
            input_prompt = """
            You are an expert news summarizer. Summarize the following text from a news website:
            Text: {text}
            """
            summary = get_gemini_response(input_prompt.format(text=content))
            st.subheader("News Summary")
            st.write(summary)
        else:
            st.write("Failed to retrieve content from the provided URL.")
    else:
        st.write("Please enter a valid URL from The Hindu.")
