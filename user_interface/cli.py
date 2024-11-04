# user_interface/cli.py
from database.db_manager import retrieve_reviews

def display_interface():
    while True:
        # Display options and retrieve/filter reviews
        user_choice = input("Choose an option: ")
        # Handle user choices
