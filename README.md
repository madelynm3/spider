# spider

## Purpose
Develop a web scraper designed to extract movie reviews from various websites. This tool will enable efficient data collection for research, analysis, and decision-making, addressing the need for comprehensive insights into film criticism.

## Description
This project will involve building a web scraper that navigates the specified websites, extracts movie review data, and stores it in formats such as CSV, JSON, or directly in a database. The project will utilize Beautiful Soup, a Python library tailored for parsing HTML and XML documents. 
- Key features:
  - Configurable data extraction based on user-defined parameters
  - Support for multiple output formats, including databases like SQLite or PostgreSQL.
  - Error handling for common web scraping issues (e.g., broken links, access restrictions)

## New Concepts
- Advanced usage of Beautiful Soup for complex data parsing specific to movie reviews.
- Techniques for handling and storing large datasets of reviews.
- Implementing web scraping ethics, including respect for `robots.txt` and rate limiting

## Resources
- **Hardware:** Computer with internet access
- **Software:** Python, Beautiful Soup, libraries for data storage (e.g., Pandas), text editor/IDE
- **Estimated Costs:** Minimal, primarily software tools (most are free or open-source)

## Dependencies
- Installation of Python and necessary libraries (requests, Beautiful Soup, etc.)
- Access to target websites for data extraction:
  - IMDb (Internet Movie Database): IMDb
  - Rotten Tomatoes: Rotten Tomatoes
  - Metacritic: Metacritic
  - Letterboxd: Letterboxd
  - FilmAffinity: FilmAffinity
  - The Guardian Film Section: The Guardian
  - RogerEbert.com: Roger Ebert
  - NPR Movies: NPR Movies
  - Collider: Collider
  - Screen Rant: Screen Rant


## Risks
- Potential website restrictions that may prevent scraping
- Changes in website structure could affect the crawling logic
- Legal considerations regarding data scraping from specific sites

## Milestones
- **Sprint 1: Project Setup** (9/30)  
  Research best practices in web scraping and finalize project scope.
  
- **Sprint 2: Development of Basic Web Crawler** (10/14)  
  Implement basic crawling functionality using Beautiful Soup.
  
- **Sprint 3: Data Extraction Logic** (10/28)  
  Develop algorithms to extract specified data points from target websites.
  
- **Sprint 4: Data Storage Implementation** (11/11)  
  Implement data storage options (CSV, JSON, database).
  
- **Sprint 5: Testing and Debugging** (11/25)  
  Conduct thorough testing and fix identified issues.
  
- **Sprint 6: Final Presentation and Documentation** (12/9)  
  Prepare documentation and present the final project to stakeholders.


## Progress
**Total Hours:** 120

- **W1:** 0
- **W2:** 3
- **W3:** 10

### Remaining Hours
**107 hours remaining**


# Movie Reviews Project

## Code Snippets with References

### main.py

```python
from scraper.scraper import scrape_reviews
from user_interface.cli import display_interface
from config import CONFIG

def main():
    # Start the scraping process and interface
    scrape_reviews(CONFIG['websites'])  # Modularity: Separate scraping logic
    display_interface()                   # Clarity: Clear function purpose

if __name__ == '__main__':
    main()
```
### config.py
```python
# Central configuration settings for easy adjustments
CONFIG = {
    'database': 'reviews.db',
    'websites': [
        "https://www.imdb.com",
        # Add more websites
    ],
}
```
Benefit: Clarity — Keeps all configurations in one place, making it easy to modify settings without digging through the code.

### scraper/scraper.py
```python
import requests
from .parser import parse_reviews  # Reusability: Use parsing logic in multiple places
from .compliance import check_compliance  # Clarity: Clear function for compliance checks
from database.db_manager import store_reviews  # Modularity: Separate database interaction

def scrape_reviews(websites):
    for website in websites:
        if check_compliance(website):  # Compliance check
            html_content = fetch_html(website)  # Fetch HTML
            reviews = parse_reviews(html_content)  # Reusable parsing function
            store_reviews(reviews)  # Modular database function

```

### database/db_manager.py

```python
import sqlite3
from config import CONFIG

def setup_database():
    # Set up the database structure
    conn = sqlite3.connect(CONFIG['database'])  # Clarity: Explicit database name from config
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (...)''')
    conn.commit()
    return conn

def store_reviews(reviews):
    conn = setup_database()  # Modularity: Isolated database setup
    cursor = conn.cursor()
    # Insert reviews into the database
    conn.commit()
    conn.close()
```

### sentiment/sentiment_analysis.py
```python
from textblob import TextBlob

def analyze_sentiment(review_text):
    # Perform sentiment analysis using TextBlob
    return TextBlob(review_text).sentiment.polarity  # Clarity: Simple function for specific task

```

Benefit: Reusability — This function can be reused across different parts of the application.

### user_interface/cli.py
```python
from database.db_manager import retrieve_reviews

def display_interface():
    while True:
        print("1. Filter reviews by title")
        print("2. Filter reviews by rating")
        print("3. Filter reviews by date")
        print("4. Exit")
        
        user_choice = input("Choose an option: ")
        
        if user_choice == '1':
            title = input("Enter movie title: ")
            reviews = retrieve_reviews(f"movie_title = '{title}'")  # Modular data retrieval
            display_reviews(reviews)
        # More options...
```
