from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.imdb.com/chart/top/"

result = requests.get(url)
page = BeautifulSoup(result.content, "html.parser")
scraped_movies = page.find_all('td', class_='titleColumn')

movies = []
for movie in scraped_movies:
    title_element = movie.find('h3')
    if title_element:
        movies.append(title_element.get_text().strip())
print(movies)
