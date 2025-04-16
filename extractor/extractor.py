import re
import spacy

# Load spaCy model (download first time: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")


def extract_info(text):
    doc = nlp(text)
    data = {
        "emails": list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))),
        "phones": list(set(re.findall(r"(\+?\d[\d\s\-().]{7,}\d)", text))),
        "addresses": [],
        "names": [],
        "social_links": extract_social_links(text),
        "services": extract_services(text)
    }

    # Pull names & orgs (basic version)
    for ent in doc.ents:
        if ent.label_ in ["PERSON"]:
            data["names"].append(ent.text)
        elif ent.label_ == "ORG" and "business_name" not in data:
            data["business_name"] = ent.text

    return data


def extract_social_links(text):
    links = {
        "linkedin": re.findall(r"(https?://(www\.)?linkedin\.com/[^\s]+)", text),
        "facebook": re.findall(r"(https?://(www\.)?facebook\.com/[^\s]+)", text),
        "twitter": re.findall(r"(https?://(www\.)?twitter\.com/[^\s]+)", text),
        "instagram": re.findall(r"(https?://(www\.)?instagram\.com/[^\s]+)", text),
    }
    return {platform: [link[0] for link in found] for platform, found in links.items() if found}


def extract_services(text):
    keywords = [
        "consulting", "coaching", "web design", "marketing", "accounting",
        "therapy", "real estate", "IT support", "software development"
    ]
    found_services = [kw for kw in keywords if kw.lower() in text.lower()]
    return found_services