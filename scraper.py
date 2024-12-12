# Importing required libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Assigning the URL
url = 'https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,asc'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

#print(soup.prettify())
#print(response.status_code)  # Should be 200
#print(response.text[:1000])  # Print a snippet of the HTML


# Creating empty lists to store data
movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
description = []
Director = []
Stars = []

# Extracting movie data
movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

for store in movie_data:
    # Movie name
    title_element = store.find('h3', class_='ipc-title__text')
    name = title_element.text.strip() if title_element else 'N/A'
    movie_name.append(name)

    # Year of release
    year_of_release = store.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
    year.append(year_of_release)

    # Runtime
    runtime = store.p.find('span', class_='runtime')
    runtime = runtime.text.replace(' min', '') if runtime else 'N/A'
    time.append(runtime)

    # Rating
    rate = store.find('div', class_='inline-block ratings-imdb-rating')
    rate = rate.text.replace('\n', '') if rate else 'N/A'
    rating.append(rate)

    # Metascore
    meta = store.find('span', class_='metascore')
    metascore.append(meta.text.strip() if meta else 'N/A')

    # Votes and Gross earnings
    value = store.find_all('span', attrs={'name': 'nv'})
    vote = value[0].text if value else 'N/A'
    votes.append(vote)
    gross_val = value[1].text if len(value) > 1 else 'N/A'
    gross.append(gross_val)

    # Description
    describe = store.find_all('p', class_='text-muted')
    description_text = describe[1].text.strip() if len(describe) > 1 else 'N/A'
    description.append(description_text)

    # Director and Stars
    cast = store.find('p', class_='')
    if cast:
        cast = cast.text.strip().split('|')
        cast = [x.strip() for x in cast]
        cast = [cast[i].replace(j, "") for i, j in enumerate(["Director:", "Stars:"])]
        Director.append(cast[0])
        Stars.append([x.strip() for x in cast[1].split(',')] if len(cast) > 1 else [])
    else:
        Director.append('N/A')
        Stars.append([])

# Creating a DataFrame
movie_df = pd.DataFrame({
    'Name of movie': movie_name,
    'Year of release': year,
    'Watchtime (min)': time,
    'Movie Rating': rating,
    'Metascore': metascore,
    'Votes': votes,
    'Gross collection': gross,
    'Description': description,
    'Director': Director,
    'Stars': Stars
})

# Saving the DataFrame to a CSV file
movie_df.to_csv("data/reviews/u.items.csv", index=False)

# Displaying the first few rows
print(movie_df.head())