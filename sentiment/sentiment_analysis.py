# sentiment/sentiment_analysis.py
from textblob import TextBlob

def analyze_sentiment(review_text):
    return TextBlob(review_text).sentiment.polarity
