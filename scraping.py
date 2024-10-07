from bs4 import BeautifulSoup
import requests

url = "https://www.rogerebert.com/reviews/megalopolis"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# Find the rating elements
# Inspect the page to find the correct tag and class name
ratings = doc.find_all("span", class_="star-box")

for rating in ratings:
    print(rating.text.strip())


# with open("index.html", "r") as f:
#     doc = BeautifulSoup(f, "html.parser")

# print(doc.prettify())

# Locate tags
# tag = doc.title
# print(tag)

# Access string within tag
# tag = doc.title
# tag.string = "hello"
# print(tag)

# Locate tags
# tags = doc.find_all("p")[0]
# print(tags.find_all("b"))

