
import random
import datetime
from tinydb import TinyDB, Query

from openai import OpenAI,api_key
import os
from dotenv import load_dotenv

# Initialize TinyDB
# db = TinyDB('mock_tweets.json')

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
api_key = API_KEY

client = OpenAI()

def analyze_tweets(me,market):
    # tweets = db.all()
    analysis_prompt = f"Analyze both my feelings:{me} and market general trend{market} and give me an insight about what to do. Use maximum 5 words. Eg You need to take profit or Make a new trade! or You are not thinking straight!"
    # tweet_texts = "\n".join([t['content'] for t in tweets])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are my personal data analyst and a psychologist.You can use maximum 5 words"},
                  {"role": "user", "content": f"{analysis_prompt}\n "}]
    )
    
    insights = response.choices[0].message.content 
    return insights

# insights = analyze_tweets("Bitcoin volatility trends upward.","Excitement versus anxiety.")
# print("Trades Analysis:", insights)