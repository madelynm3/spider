from scraper.scraper import scrape_reviews
from user_interface.cli import display_interface
from config import CONFIG

def main():
    scrape_reviews(CONFIG['websites'])
    display_interface()

if __name__ == '__main__':
    main()
