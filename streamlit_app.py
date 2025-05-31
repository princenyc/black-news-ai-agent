import streamlit as st
import requests
import openai

openai.api_type = "azure"
openai.api_key = st.secrets["AZURE_OPENAI_KEY"]
openai.api_base = st.secrets["AZURE_OPENAI_ENDPOINT"]
openai.api_version = "2023-05-15"

AZURE_OPENAI_DEPLOYMENT = st.secrets["AZURE_OPENAI_DEPLOYMENT"]
BING_NEWS_KEY = st.secrets["BING_NEWS_KEY"]
BING_NEWS_ENDPOINT = "https://api.bing.microsoft.com/v7.0/news/search"

def fetch_news():
    headers = {"Ocp-Apim-Subscription-Key": BING_NEWS_KEY}
    params = {
        "q": "Black Americans OR African Americans",
        "count": 15,
        "mkt": "en-US",
        "sortBy": "Date"
    }
    res = requests.get(BING_NEWS_ENDPOINT, headers=headers, params=params)
    return res.json().get("value", [])

def summarize_news(articles):
    news_text = "\n\n".join([
        f"Title: {a['name']}\nDesc: {a.get('description', '')}\nURL: {a['url']}"
        for a in articles
    ])
    prompt = f"""
You are a news summarization agent for a Black-focused newsletter. From the articles below, choose the **top 5** stories most relevant to Black Americans today. Summarize each in 2 sentences and include the link.

{news_text}
    """
    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]

def main():
    st.title("📰 Top 5 News Stories for Black Americans")
    st.caption("Powered by Bing News & Azure OpenAI")
    
    with st.spinner("Fetching and analyzing the latest news..."):
        articles = fetch_news()
        summary = summarize_news(articles)

    st.markdown("### 🧠 Curated Summary")
    st.markdown(summary)

if __name__ == "__main__":
    main()
