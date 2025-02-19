
import random
import datetime
from tinydb import TinyDB, Query

from openai import OpenAI,api_key
import os
from dotenv import load_dotenv

# Initialize TinyDB
db = TinyDB('mock_tweets.json')

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
api_key = API_KEY

client = OpenAI()

def generate_mock_tweet():
    """Generates a mock tweet using OpenAI's API."""
    prompt = "Generate a realistic tweet about trending topics like tech, especially about the moving price of bitcoin. Include hashtags."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a social media user generating tweets."},
                  {"role": "user", "content": prompt}]
    )
    
    tweet_text = response.choices[0].message.content 
    
    
    return {
        "username": f"user{random.randint(1000, 9999)}",
        "timestamp": datetime.datetime.now().isoformat(),
        "content": tweet_text,
        "likes": random.randint(0, 5000),
        "retweets": random.randint(0, 2000),
        "hashtags": [word for word in tweet_text.split() if word.startswith("#")]
    }

# Generate and store 10 mock tweets
for _ in range(10):
    tweet = generate_mock_tweet()
    db.insert(tweet)

print("Mock tweets generated and stored in TinyDB!")

# tweet = generate_mock_tweet()
# print(tweet)