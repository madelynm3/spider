import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,asc"

# Send GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all movie titles
movies = soup.find_all('h3', class_='lister-item-header')

print(movies)
