import requests
import time
from bs4 import BeautifulSoup
import re
import json


class WikipediaScraper:

    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookie_endpoint = "/cookie"
        self.leaders_data = {}
        self.cookie = None

        # Wikipedia session 
        self.wiki_session = requests.Session()
        self.user_agent = {
            "User-Agent": "wikipediascraper/1.0 (student project; contact: jonbesh.ahmadzai@gmail.com)"
        }
        self.wiki_session.headers.update(self.user_agent)

    def safe_get(self, url, **kwargs):
        try:
            return requests.get(url, **kwargs)
        except requests.RequestException:
            return None

    def refresh_cookie(self):
        response = self.safe_get(self.base_url + self.cookie_endpoint, timeout=20)
        if response is None or response.status_code != 200:
            return None

        self.cookie = response.cookies.get_dict()
        return self.cookie

    def get_countries(self):
        if self.cookie is None:
            if self.refresh_cookie() is None:
                return []

        response = self.safe_get(
            self.base_url + self.country_endpoint,
            cookies=self.cookie,
            timeout=20
        )
        if response is None or response.status_code != 200:
            return []

        data = response.json()
        return data if isinstance(data, list) else []

    def get_leaders(self, country: str) -> None:
        if self.cookie is None:
            if self.refresh_cookie() is None:
                self.leaders_data[country] = []
                return

        params = {"country": country}

        response = self.safe_get(
            self.base_url + self.leaders_endpoint,
            cookies=self.cookie,
            params=params,
            timeout=20
        )

        # If request failed (cookie can expire), refresh once and retry
        if response is None or response.status_code != 200:
            if self.refresh_cookie() is None:
                self.leaders_data[country] = []
                return

            response = self.safe_get(
                self.base_url + self.leaders_endpoint,
                cookies=self.cookie,
                params=params,
                timeout=20
            )

            if response is None or response.status_code != 200:
                self.leaders_data[country] = []
                return

        data = response.json()
        if not isinstance(data, list):
            self.leaders_data[country] = []
            return

        enriched_leaders = []

        for leader in data:
            wiki_url = leader.get("wikipedia_url")

            if wiki_url:
                paragraph = self.get_first_paragraph(wiki_url)
                time.sleep(1.0)  # polite delay to reduce Wikipedia rate-limiting
            else:
                paragraph = None

            leader["paragraph"] = paragraph
            enriched_leaders.append(leader)

        self.leaders_data[country] = enriched_leaders

    def get_first_paragraph(self, wikipedia_url: str):
        if not wikipedia_url:
            return None

        try:
            response = self.wiki_session.get(wikipedia_url, timeout=20)
        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        for p in paragraphs:
            text = p.get_text().strip()
            if not text:
                continue

            cleaned = re.sub(r"\[\d+\]|\[[a-z]\]", "", text)
            cleaned = re.sub(r"\xa0", " ", cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()

            low = cleaned.lower()


            # "good paragraph" checks
            if len(cleaned) > 80 and "." in cleaned and "may refer to" not in low and ":" not in cleaned[:40]:
                return cleaned

        return None

    def to_json_file(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.leaders_data, f, ensure_ascii=False, indent=2)

        print(f"Data saved to {filepath}")

        # verify
        with open(filepath, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        if self.leaders_data == loaded_data:
            print("Data successfully matched perfectly!")
        else:
            print("Data mismatch!")