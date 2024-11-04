# scraper/scraper.py
import requests
from .parser import parse_reviews
from .compliance import check_compliance
from database.db_manager import store_reviews

def scrape_reviews(websites):
    for website in websites:
        if check_compliance(website):
            html_content = fetch_html(website)
            reviews = parse_reviews(html_content)
            store_reviews(reviews)
