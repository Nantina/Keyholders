import os
from flask import Flask, request, jsonify
import openai


app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

def analyze_trade_data(data):

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        message=[
            {"role": "user", "content": "Question"}
        ]
    )

    return response

@app.route("/")
def home():
    return "Test Flask App"

@app.route("/analyze")
def health_check():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
