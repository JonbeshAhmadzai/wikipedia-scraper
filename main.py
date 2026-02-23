from src.scraper import WikipediaScraper


def main():
    scraper = WikipediaScraper()

    countries = scraper.get_countries()
    print("countries length:", len(countries))
    print("countries preview:", countries[:10])

    for code in countries:
        print(f"Fetching leaders for: {code}")
        scraper.get_leaders(code)
        print("Countries saved so far:", len(scraper.leaders_data))

    scraper.to_json_file("leaders.json")
    print("Saved leaders.json")
    print("Countries saved:", len(scraper.leaders_data))


if __name__ == "__main__":
    main()