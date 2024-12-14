# Importing required libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Assigning the URL
url = 'https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,asc'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# Making the request with a small delay to be polite
time.sleep(1)
response = requests.get(url, headers=headers)

# Creating the soup object
soup = BeautifulSoup(response.content, 'html.parser')

# Creating empty lists to store data
movie_name = []
year = []
time_duration = []
rating = []
metascore = []
votes = []
gross = []
description = []
Director = []
Stars = []

# Finding all movie containers
movie_data = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')

for store in movie_data:
    # Movie name
    name = store.find('h3', class_='ipc-title__text')
    name = name.text.strip() if name else 'N/A'
    movie_name.append(name)

    # Year of release
    year_element = store.find('span', class_='sc-300a8231-7 eaXxft dli-title-metadata-item')
    year_text = year_element.text.strip() if year_element else 'N/A'
    # Extract just the year using regex if needed
    year.append(year_text)

    # Runtime
    runtime = store.find('span', class_='runtime')
    runtime = runtime.text.replace(' min', '') if runtime else 'N/A'
    time_duration.append(runtime)

    # Rating
    rate = store.find('span', class_='ipc-rating-star--rating')
    #rate = rate['aria-label'].split()[0] if rate else 'N/A'
    rating.append(rate.text.strip() if rate else 'N/A')

    # Metascore
    meta = store.find('span', class_='sc-b0901df4-0 bXIOoL metacritic-score-box')
    metascore.append(meta.text.strip() if meta else 'N/A')

    # Description
    desc = store.find('div', class_='ipc-html-content-inner-div')
    description.append(desc.text.strip() if desc else 'N/A')

    # Director and Stars
    credit_info = store.find_all('span', class_='ipc-metadata-list-item__list-content-item')

    if credit_info:
        Director.append(credit_info[0].text if len(credit_info) > 0 else 'N/A')
        Stars.append([star.text for star in credit_info[1:]] if len(credit_info) > 1 else [])
    else:
        Director.append('N/A')
        Stars.append([])

    # Votes and Gross (these might need adjustment based on actual HTML structure)
    vote_element = store.find('span', {'name': 'nv'})
    votes.append(vote_element.text if vote_element else 'N/A')

    gross_element = store.find('span', string=lambda text: text and '$' in text if text else False)
    gross.append(gross_element.text if gross_element else 'N/A')

# Creating a DataFrame
movie_df = pd.DataFrame({
    'Name of movie': movie_name,
    'Year of release': year,
    #'Watchtime (min)': time_duration,
    'Movie Rating': rating,
    'Metascore': metascore,
    #'Votes': votes,
    #'Gross collection': gross,
    'Description': description,
    #'Director': Director,
    #'Stars': Stars
})

# Display the first few rows
print(movie_df.head())

# Save to CSV if needed
movie_df.to_csv("data/reviews/u.items.csv", index=False)