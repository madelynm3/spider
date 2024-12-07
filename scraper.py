import pandas as pd
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
from imdb import IMDb

def get_imdb_url(movies):
    ia = IMDb()

    movie_ids = []
    movie_years = []
    movie_titles = []
    imdb_urls = ['https://www.imdb.com/chart/top/']
    
    for index in range(0, len(movies)-1):
        movie_id = movies['movie_id'][index]
        movie_year = movies['year'][index]
        movie_title = movies['stripped_title'][index]                

        # Search for the movie
        search_results = ia.search_movie(movie_title)

        if not search_results:
            print(f"Movie '{movie_title}' not found on IMDb.")
            continue

        movieid = search_results[0].movieID
        movie = ia.get_movie(movieid)
        movie_url = ia.get_imdbURL(movie)
        
        movie_ids.append(movie_id)
        movie_years.append(movie_year)
        movie_titles.append(movie_title)
        imdb_urls.append(movie_url)

    print(f"Length of movie_ids: {len(movie_ids)}")
    print(f"Length of movie_years: {len(movie_years)}")
    print(f"Length of movie_titles: {len(movie_titles)}")
    print(f"Length of imdb_urls: {len(imdb_urls)}")

    # Build data dictionary for dataframe
    data = {'movie_id': movie_ids, 
            'movie_year': movie_years, 
            'stripped_title': movie_titles,
            'imdb_url' : imdb_urls
    }
    
    # Ensure the 'data' directory exists before saving
    if not os.path.exists('data'):
        os.makedirs('data')

    # Build dataframe for each movie to export
    movies_data = pd.DataFrame(data)
    
    # Save URLs in a CSV file
    movies_data.to_csv('data/moviesurl.csv', index=False)

    return movies_data  # Ensure to return the dataframe


def get_review(url_df, folder_name):
    PATH = r"C:/chromedriver/chromedriver.exe"  # path to the webdriver file
    title = []
    link = url_df['imdb_url']
    year = []      

    user_review_links = []
    for i in range(len(url_df)):
        review_link = url_df['imdb_url'][i] + 'reviews/?ref_=tt_ql_2'
        user_review_links.append(review_link)

    url_df['review_link'] = user_review_links
    
    # Create folder to store reviews if not exist
    if not os.path.exists(f'data/{folder_name}'):
        os.makedirs(f'data/{folder_name}')

    for i in range(len(url_df['review_link'])): 
        service = Service(PATH)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"Scraping reviews for {url_df['stripped_title'][i]}")

        try:
            driver.get(url_df['review_link'][i])
            driver.implicitly_wait(10)  # Adjust wait time based on page load speed

            page = 1  # Start with the first page of reviews
            while page < 50:  # Grab reviews until we have enough
                try:
                    load_more = driver.find_element(By.ID, 'load-more-trigger')
                    load_more.click()
                    page += 1
                except:
                    print(f"No more reviews to load for {url_df['stripped_title'][i]} on page {page}")
                    break

            reviews = driver.find_elements(By.CLASS_NAME, 'review-container')
            title, content, rating, date, user_name = [], [], [], [], []

            for review in reviews:
                try:
                    ftitle = review.find_element(By.CLASS_NAME, 'title').text
                    fcontent = review.find_element(By.CLASS_NAME, 'content').get_attribute("textContent").strip()
                    frating = review.find_element(By.CLASS_NAME, 'rating-other-user-rating').text
                    fdate = review.find_element(By.CLASS_NAME, 'review-date').text
                    fname = review.find_element(By.CLASS_NAME, 'display-name-link').text
                    
                    title.append(ftitle)
                    content.append(fcontent)
                    rating.append(frating)
                    date.append(fdate)
                    user_name.append(fname)
                except Exception as e:
                    continue  # If there's an error, skip the review

            data = {
                'User_name': user_name, 
                'Review title': title, 
                'Review Rating': rating,
                'Review date': date,
                'Review_body': content
            }

            review_df = pd.DataFrame(data)
            movie = url_df['stripped_title'][i]    
            review_df['Movie_name'] = movie
            review_df['movie_id'] = url_df['movie_id'][i]

            review_df.to_csv(f'data/{folder_name}/{url_df["movie_id"][i]}.csv', index=False)
        except Exception as e:
            print(f"Error scraping {url_df['stripped_title'][i]}: {str(e)}")
        finally:
            driver.quit()

    print("Done processing all reviews.")


if __name__ == '__main__':
    # Load movie data
    col_names = ['movie_id',
                 'movie_title',
                 'release_date',
                 'video_release_date',
                 'imdb_url',
                 'unknown',
                 'action',
                 'adventure',
                 'animation',
                 'children',
                 'comedy',
                 'crime',
                 'documentary',
                 'drama',
                 'fantasy',
                 'film_noir',
                 'horror',
                 'musical',
                 'mystery',
                 'romance',
                 'sci_fi',
                 'thriller',
                 'war',
                 'western']

    movies = pd.read_csv('u.item.csv', sep='|', header=None, names=col_names, encoding='ISO-8859-1')

    # Ensure 'movie_title' is treated as string
    movies['movie_title'] = movies['movie_title'].fillna('').astype(str)
    
    # Fix the regular expression to extract the year correctly
    movies['year'] = movies['movie_title'].str.extract(r'.*\((\d{4})\).*', expand=False)
    movies['stripped_title'] = movies['movie_title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True)

    # Retrieve movie IMDb URL
    urls = get_imdb_url(movies)
    print("!!! Done retrieving links !!!")

    # Scrape movie reviews
    movies_imdb = pd.read_csv('data/moviesurl.csv')
    movies_imdb = movies_imdb.drop(movies_imdb.columns[movies_imdb.columns.str.contains('Unnamed', case=False)], axis=1)

    get_review(movies_imdb, 'reviews')
