from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

def scrape_imdb_top_250():
    # Setup WebDriver
    PATH = "C:/chromedriver/chromedriver.exe"
    service = Service(PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # Go to the IMDb Top 250 page
    url = "https://www.imdb.com/chart/top"
    driver.get(url)

    # Allow the page to load
    time.sleep(3)

    # Find the movie elements on the page
    movies = driver.find_elements(By.CSS_SELECTOR, '.lister-list .titleColumn a')

    movie_ids = []
    movie_titles = []
    imdb_urls = []

    # Iterate through the movie elements and extract information
    for movie in movies:
        movie_title = movie.text
        movie_url = movie.get_attribute("href")
        movie_id = movie_url.split('/')[4]  # Extract movie ID from URL (e.g., tt1234567)

        # Append to lists
        movie_ids.append(movie_id)
        movie_titles.append(movie_title)
        imdb_urls.append(movie_url)

    # Close the WebDriver
    driver.quit()

    # Create a DataFrame with the extracted movie information
    data = {
        'movie_id': movie_ids,
        'movie_title': movie_titles,
        'imdb_url': imdb_urls
    }

    top_movies_df = pd.DataFrame(data)

    # Ensure the 'data' directory exists before saving
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save to a CSV file
    top_movies_df.to_csv('data/top_imdb_movies.csv', index=False)

    return top_movies_df

# Run the scraping function to get the top 250 IMDb movies
top_movies_df = scrape_imdb_top_250()
print(top_movies_df.head())  # Show the top movies
