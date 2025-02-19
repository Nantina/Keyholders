from fastapi import FastAPI
import uvicorn
from tinydb import TinyDB
import pandas as pd
import analyze_my_sentiment as an
import analyze_ai as an1
import analyze_me
import analyze_market
import personal_insight

import assistant_submit 

app = FastAPI()

# Db journal
db_journal = TinyDB('mock_journal.json')

#DB tweets
db_tweets = TinyDB('mock_tweets.json')

#Fake in memory sentiments
sentiments = [{"ticker": "AAPL", "sentiment": 0.75}, {"ticker": "TSLA", "sentiment": -0.2}]




@app.get("/")
def read_root():
    return{"message": "Trading Sentiment API Running!"}

@app.get("/sentiments")
def get_sentiments():
    return {"data": sentiments }

@app.get("/history")
def get_history():
     #Fake trading journal
    journal_entries = db_journal.all()
    if journal_entries:
        df = pd.DataFrame(journal_entries)
    return df

@app.get("/my_analysis")
def get_analysis_me():
    # Analyze my journal
    journal_entries = db_journal.all()
    if journal_entries:
        # call gpt to analyze past trades
        response = an.analyze_journal()
        return response
    else:
        return "Empty db"

@app.get("/fear_greed")
def get_fg():
    tweets = db_tweets.all()
    if tweets:
        response = an1.analyze_tweets()
        return response
    else:
        return "Empty tweets"


# Endpoint for mock journal submitions
@app.get("/submit-mock")
def get_ai_submit():
    resp = assistant_submit.submit_fake()
    return resp

@app.get("/me")
def get_my_thoughts():
    resp = analyze_me.analyze_mine()
    return resp

@app.get("/market")
def get_my_thoughts():
    resp = analyze_market.analyze_tweets()
    return resp

@app.get("/me_market")
def get_insight():
    resp = personal_insight.analyze_tweets(analyze_me.analyze_mine(),analyze_market.analyze_tweets())
    return resp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)