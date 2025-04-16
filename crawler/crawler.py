import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""


def crawl_website(start_url, max_pages=30):
    visited = set()
    to_visit = [start_url]
    base_domain = urlparse(start_url).netloc
    all_pages = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            print(f"Crawling: {url}")
            response = requests.get(url, timeout=20)
            if response.status_code != 200:
                continue

            visited.add(url)
            all_pages.append(url)

            soup = BeautifulSoup(response.text, "lxml")
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if is_valid_url(full_url, base_domain) and full_url not in visited:
                    to_visit.append(full_url)

        except Exception as e:
            print(f"Error visiting {url}: {e}")

    return all_pages