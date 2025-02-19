
import random
import datetime
from tinydb import TinyDB, Query

from openai import OpenAI,api_key
import os
from dotenv import load_dotenv

# Initialize TinyDB
db = TinyDB('mock_journal.json')

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
api_key = API_KEY

client = OpenAI()

def analyze_mine():
    tweets = db.all()
    analysis_prompt = "Analyze these journal entries to explain my general feelings. Find correlations between emotions and profitability. Summarize insights.Use maximum 3 words"
    # entries = "\n".join([t for t in tweets])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are my personal data analyst and a psychologist.You can use maximum 3 words"},
                  {"role": "user", "content": f"{analysis_prompt}\n {tweets}"}]
    )
    
    insights = response.choices[0].message.content 
    return insights

# insights = analyze_mine()
# print("Trades Analysis:", insights)