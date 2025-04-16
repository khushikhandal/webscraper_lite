#uvicorn main:app --reload
#http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from crawler.crawler import crawl_website
from scraper.page_scraper import get_visible_text_from_url
from extractor.llm_extractor import extract_info_with_llm

# Create FastAPI app instance
app = FastAPI()

# Request body model
class WebsiteRequest(BaseModel):
    url: str

# Function that wraps the existing logic
def scrape_and_extract_info(website: str):
    # Crawl the website for pages
    pages = crawl_website(website, max_pages=5)

    results = []
    os.makedirs("output", exist_ok=True)

    raw_output_path = "output/raw_llm_outputs.txt"
    # Clear existing raw output file before appending
    open(raw_output_path, "w").close()

    for page in pages:
        page_data = get_visible_text_from_url(page)
        if not page_data:
            continue

        # Extract info using the LLM
        extracted, raw = extract_info_with_llm(page_data["text"], model="tinyllama")

        results.append({
            "url": page,
            "title": page_data["title"],
            "data": extracted
        })

        # Append raw output to a .txt file
        with open(raw_output_path, "a", encoding="utf-8") as raw_file:
            raw_file.write(f"=== RAW OUTPUT FOR: {page} ===\n")
            raw_file.write(raw)
            raw_file.write("\n\n")

    # Saving the results as JSON
    output_path = "output/extracted_business_profiles.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results, output_path

# API endpoint to scrape and extract business profiles
@app.post("/extract_profiles")
async def extract_profiles(request: WebsiteRequest):
    try:
        website = request.url.strip()
        results, output_path = scrape_and_extract_info(website)
        return {"message": "Extraction complete", "data": results, "output_file": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))