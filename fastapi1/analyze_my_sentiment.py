
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

def analyze_journal():
    tweets = db.all()
    analysis_prompt = "Analyze these journal entries for common sentiment and trends. Find correlations between emotions and profitability. Summarize insights."
    # entries = "\n".join([t for t in tweets])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are my personal data analyst and a psychologist."},
                  {"role": "user", "content": f"{analysis_prompt}\n {tweets}"}]
    )
    
    insights = response.choices[0].message.content 
    return insights

# insights = analyze_journal()
# print("Trades Analysis:", insights)