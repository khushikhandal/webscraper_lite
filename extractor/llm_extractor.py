import requests
import json

# Prompt Template
PROMPT_TEMPLATE = """
You are an AI assistant helping to extract business information from a website page.
Return the following fields in JSON format:
- business_name
- brief_description
- phone
- email
- address
- key_people
- services
- fees
- social_links

Here is the page content:
\"\"\"
{text}
\"\"\"

JSON Output:
"""

def extract_info_with_llm(text, model="tinyllama"):
    prompt = PROMPT_TEMPLATE.format(text=text[:4000])  # truncate if too long

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        print(f"Error from Ollama: {response.status_code}")
        return {}, ""

    raw_output = response.json()["response"].strip()

    # Try to parse JSON
    try:
        json_data = json.loads(raw_output)
        return json_data, raw_output
    except Exception as e:
        print("⚠️ Failed to parse JSON output:", e)
        #print("🔎 Raw LLM Output:", raw_output)
        return {}, raw_output

"""
    if response.status_code != 200:
        print(f"Error from Ollama: {response.status_code}")
        return {}

    try:
        raw_output = response.json()["response"].strip()
        json_data = json.loads(raw_output)
        return json_data
    except Exception as e:
        print("Failed to parse JSON output:", e)
        print("Raw LLM Output:", raw_output)
        return {}
"""
