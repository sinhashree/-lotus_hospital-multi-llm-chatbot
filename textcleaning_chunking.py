import re
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
def clean_scraped_text(raw_html):
    # 1. Strip HTML tags
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text()
    # 2. Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # 3. Normalize whitespace and lowercase
    text = " ".join(text.split()).lower()
    
    # 4. Remove special characters (optional)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# Split by fixed number of characters
def chunk_by_chars(text, n):
    return [text[i:i+n] for i in range(0, len(text), n)]