import pandas as pd
from flask import Flask, request, jsonify
# pip install openai 
import openai


app = Flask(__name__)

# Get data
df = pd.read_csv("trading_data.csv")


API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

def analyze_trade_data(data):

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        message=[
            {"role": "user", "content": "Question"}
        ]
    )

    return response


@app.route("/analyze", methods=["POST"])
def analyze():
    trade_data = request.json.get("trade_data")
    analysis = analyze_trade_data(trade_data)
    return jsonify({"suggestion": analysis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
