import requests
from readability import Document
from bs4 import BeautifulSoup


def get_visible_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        html = response.text

        # Use readability to extract the main article-like content
        doc = Document(html)
        title = doc.short_title()
        content_html = doc.summary()

        # Strip HTML tags to get clean text
        soup = BeautifulSoup(content_html, "lxml")
        text = soup.get_text(separator="\n", strip=True)

        return {
            "url": url,
            "title": title,
            "text": text
        }

    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None