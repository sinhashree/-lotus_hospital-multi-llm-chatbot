from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

base_url = "https://www.lotushospital.co.in/"

# Step 1: Read Homepage with timeout
page = urlopen(base_url,timeout=20)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Step 2: Extract all internal hyperlinks
links = set()
for a in soup.find_all("a", href=True):
    link = a['href']
    if link.startswith("/"):
        full_link = base_url.rstrip("/") + link
        links.add(full_link)
    elif base_url in link:
        links.add(link)

# Add homepage
links.add(base_url)

print(f"Found {len(links)} pages")

all_text = ""

# Step 3: Scrape all pages
for link in links:

    # Skip unwanted links
    if ".pdf" in link:
        continue

    if "facebook" in link or "instagram" in link:
        continue

    if ".jpg" in link or ".jpeg" in link or ".png" in link:
        continue
    try:
        page = urlopen(link, timeout=20)

        html = page.read().decode("utf-8", errors="ignore")

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator=" ")

        all_text += text + "\n"

        print(f"Scraped: {link}")
    except Exception as e:
        print(f"Failed: {link}")
        print(e)

# Step 4: Clean text
all_text = re.sub(r'https?://\S+', '', all_text)
all_text = " ".join(all_text.split())
all_text = all_text.lower()

# Step 5: Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(all_text)

# Step 6: Save
with open("corpus_text.txt", "w", encoding="utf-8") as f:

    for i, chunk in enumerate(chunks):

        f.write(f"Chunk {i+1}:\n")

        f.write(chunk + "\n\n")

print(f"Saved {len(chunks)} chunks")