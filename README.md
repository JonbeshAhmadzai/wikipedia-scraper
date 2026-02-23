# 🌍 Wikipedia Political Leaders Scraper

## 📖 Overview

This project was developed during my training at **BeCode** to
strengthen my understanding of:

-   API integration\
-   Web scraping\
-   Data enrichment\
-   Object-Oriented Programming (OOP)\
-   Session & cookie management\
-   JSON serialization

The application retrieves political leaders from multiple countries via
a custom API and enriches the dataset by scraping the first meaningful
paragraph from each leader's Wikipedia page.

Each execution of the script:

1.  Retrieves a valid session cookie from the API\
2.  Fetches all supported countries\
3.  Collects leaders for each country\
4.  Scrapes and cleans the first paragraph from each leader's Wikipedia
    page\
5.  Saves the enriched dataset into a structured JSON file

The final output is stored in:

    leaders.json

------------------------------------------------------------------------

## 🏗 Architecture & Data Flow

    API (country-leaders.onrender.com)
            ↓
    Fetch Cookie
            ↓
    Get Countries
            ↓
    Get Leaders per Country
            ↓
    Scrape Wikipedia Paragraph
            ↓
    Clean & Enrich Data
            ↓
    Export to JSON

All scraping logic is encapsulated inside the `WikipediaScraper` class.

------------------------------------------------------------------------

## 🧠 OOP Concepts Demonstrated

### 🔹 Encapsulation

All scraping functionality is contained within the `WikipediaScraper`
class.

### 🔹 Abstraction

Methods such as:

-   `get_countries()`
-   `get_leaders()`
-   `get_first_paragraph()`

hide complex implementation details behind clean interfaces.

### 🔹 State Management

The class maintains internal state using:

-   `self.cookie`
-   `self.leaders_data`

### 🔹 Modularity

Each method has a single responsibility, making the code easier to
maintain and extend.

------------------------------------------------------------------------

## 🛠 Technologies Used

  Technology       Purpose
  ---------------- ---------------------------
  Python 3.10+     Core programming language
  requests         API communication
  BeautifulSoup4   HTML parsing
  re               Text cleaning
  json             Data serialization
  time             Rate control

------------------------------------------------------------------------

## 🏗 Project Structure

    wikipedia-scraper/
    │
    ├── src/
    │   ├── scraper.py              # Main WikipediaScraper class
    │   └── leaders_scraper.py      # Additional scraper logic (if applicable)
    │
    ├── main.py                     # Entry point of the application
    ├── leaders.json                # Output file (generated after running)
    ├── requirements.txt            # Python dependencies
    ├── README.md                   # Project documentation
    ├── .gitignore                  # Ignored files (e.g., .venv)
    └── wikipedia_scraper.ipynb     # Jupyter notebook (optional exploration)

⚠️ The virtual environment (`.venv/`) is excluded via `.gitignore` and
is not part of the repository.

------------------------------------------------------------------------
## 🚀 Installation

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/wikipedia-scraper.git
cd wikipedia-scraper
```

### 2️⃣ Create a virtual environment

``` bash
python -m venv .venv
```

Activate it:

Mac/Linux:

``` bash
source .venv/bin/activate
```

Windows:

``` bash
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Usage

Run the scraper:

``` bash
python main.py
```

The script will:

-   Fetch a valid API cookie\
-   Retrieve all supported countries\
-   Collect leader data\
-   Scrape Wikipedia biographies\
-   Save everything to `leaders.json`

------------------------------------------------------------------------

## 📄 Example Output

``` json
{
  "us": [
    {
      "first_name": "George",
      "last_name": "Washington",
      "birth_date": "1732-02-22",
      "wikipedia_url": "https://en.wikipedia.org/wiki/George_Washington",
      "paragraph": "George Washington was an American military officer and statesman..."
    }
  ]
}
```

------------------------------------------------------------------------

## 🛡 Stability & Ethical Scraping

This project:

-   Uses a proper custom `User-Agent`
-   Implements controlled delays between Wikipedia requests
-   Handles cookie expiration gracefully
-   Validates API responses before processing
-   Prevents saving rate-limit messages as data

The scraper respects Wikipedia's access policies and does not bypass
rate limits or robot policies.

------------------------------------------------------------------------

## 📊 Core Methods

  Method                       Description
  ---------------------------- -------------------------------------
  `safe_get()`                 Centralized request wrapper
  `refresh_cookie()`           Retrieves API session cookie
  `get_countries()`            Fetches supported countries
  `get_leaders(country)`       Retrieves leaders and enriches them
  `get_first_paragraph(url)`   Scrapes first meaningful paragraph
  `to_json_file(filepath)`     Saves dataset to JSON

------------------------------------------------------------------------

## ⏳ Development Timeline

Completed in **2 days**, including:

-   API integration\
-   HTML parsing logic\
-   Cookie/session debugging\
-   Data cleaning\
-   JSON validation

------------------------------------------------------------------------

## 🎓 Context

This project was developed during the **AI Bootcamp at BeCode.org** as
part of backend and scraping training.

------------------------------------------------------------------------

## 👨‍💻 Author

Jonbesh Ahmadzai\
AI Bootcamp -- BeCode

