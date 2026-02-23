import re
import json
import requests
from bs4 import BeautifulSoup

root_url = "https://country-leaders.onrender.com"


def get_first_paragraph(wikipedia_url, session=None):
    if not wikipedia_url:
        return None

    if session is None:
        session = requests.Session()

    headers= {"User-Agent": "Mozilla/5.0"}
    html = session.get(wikipedia_url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")

    first_paragraph = None
    for p in paragraphs:
        text = p.get_text().strip()
        if text: 
           if len(text) > 100:
               if any(c.isalpha() for c in text):
                   if "." in text:
                       if "may refer to" not in text.lower():
                         if ":" not in text[:40]:
                            first_paragraph = text
                            break 

    if first_paragraph is None:
        return None

    cleaned = re.sub(r"\[\d+\]|\[[a-z]\]", "", first_paragraph)
    cleaned = re.sub(r"\xa0", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def get_leaders_par():
    session = requests.Session()
    wiki_session = requests.Session()

    root_url = "https://country-leaders.onrender.com"
    cookie_url = root_url + "/cookie"
    countries_url = root_url + "/countries"
    leaders_url = root_url + "/leaders"
    cookies = session.get(cookie_url).cookies

    country_list = session.get(countries_url, cookies=cookies).json()
    if isinstance(country_list, dict) and "message" in country_list and "cookie" in country_list["message"].lower():
        cookies = session.get(cookie_url).cookies
        country_list = session.get(countries_url, cookies=cookies).json()

    leaders_per_country = {}

    for code in country_list:
        params = {"country": code}
        leaders = session.get(leaders_url, cookies=cookies, params=params).json()

        if isinstance(leaders, dict) and "message" in leaders and "cookie" in leaders["message"].lower():
            cookies = session.get(cookie_url).cookies
            leaders = session.get(leaders_url, cookies=cookies, params=params).json()

        if not isinstance(leaders, list):
            continue

        for leader in leaders:
            leader["country_code"] = params["country"]
            leader["paragraph"] = get_first_paragraph(leader.get("wikipedia_url"), session=wiki_session)

        leaders_per_country[code] = leaders

    return leaders_per_country


def save(leaders_per_country):
    with open("leaders.json", "w", encoding="utf-8") as f:
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    leaders_per_country = get_leaders_par()

save(leaders_per_country)
