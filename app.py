import streamlit as st
import google.generativeai as genai
from newspaper import Article

# Page config
st.set_page_config(page_title="Career-OS", layout="wide")
st.title("🚀 Career-OS: Authority Engine")

# Security: Accessing the API key from Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Advanced Settings.")
    st.stop()

url = st.text_input("Paste the URL you want to digest:")

if st.button("Synthesize Authority"):
    if url:
        with st.spinner("Digesting..."):
            try:
                article = Article(url)
                article.download()
                article.parse()
                
                prompt = f"""
                Act as a Staff Engineer and Technical Recruiter. Analyze: {article.title}
                Content: {article.text}
                
                Generate:
                1. A punchy LinkedIn Hook.
                2. 3 High-Impact Technical Bullet points (quantifiable, value-driven).
                3. A professional CTA to drive engagement.
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please provide a URL.")
