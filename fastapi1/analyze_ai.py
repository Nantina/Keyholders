
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

def analyze_tweets():
    tweets = db.all()
    analysis_prompt = "Analyze these tweets for common topics, sentiment, and trends. Summarize insights.In one sentence at the end make a prediction of the price movement based on these trends."
    tweet_texts = "\n".join([t['content'] for t in tweets])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a data analyst. You make it clear if I should buy or sell right now"},
                  {"role": "user", "content": f"{analysis_prompt}\n{tweet_texts}"}]
    )
    
    insights = response.choices[0].message.content 
    return insights

# insights = analyze_tweets()
# print("Tweet Analysis:", insights)