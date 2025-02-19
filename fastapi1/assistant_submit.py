from openai import OpenAI,api_key
import os
from dotenv import load_dotenv
from tinydb import TinyDB
import json

from typing import Literal,Dict
from datetime import datetime




load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
api_key = API_KEY



def submit_fake():
  # Upload a file with an "assistants" purpose
  client = OpenAI()
  file1 = client.files.create(
    file=open("buy.json", "rb"),
    purpose='assistants'
  )
  # Upload a file with an "assistants" purpose
  file2 = client.files.create(
    file=open("sell.json", "rb"),
    purpose='assistants'
  )


  # create an assistant
  assistant = client.beta.assistants.create(
    name="Assistant1",
    instructions="You are a trader. Write and run code to answer questions.Output in json",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    
  )

  # create a thread
  thread = client.beta.threads.create()

  # Add a Message to the Thread
  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Generate two realistic Bitcoin trade journal entries in JSON format.Include datetime, buy/sell type, price, amount, total cost or revenue, trader's thoughts with emotions (e.g., nervousness, excitement, doubt), and profit/loss. Make it like buy.json and sell.json.Provide only the json as a file and nothing else",
    
    attachments= [
          {
            "file_id": file1.id,
            "tools": [{"type": "code_interpreter"}]
          },
          {
            "file_id": file2.id,
            "tools": [{"type": "code_interpreter"}]
          }
        ]
        
    
  )

  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="The user has a premium account."
  )

  if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    # print(messages)
    # Extract file_ids
    
    file_ids = [attachment.file_id for message in messages.data for attachment in message.attachments]
    print(file_ids)
    
    for c in file_ids:
      try:
        data = client.files.content(c)
        data_bytes = data.read()
        print(data_bytes)
        # Then add it to db
        # db = TinyDB('mock_journal.json')
        # db.insert(json.loads(data_bytes))
        print(json.loads(data_bytes))
        clean_trade_entry(json.loads(data_bytes))
        
      except Exception as f:
        print(f"assistants error{f}")
    return "Submitted!"

  else:
    print(run.status)

def clean_trade_entry(data: dict) -> dict:
    """Ensure the trade entry follows the required template."""
    required_keys = {"datetime", "trade_type", "price", "amount", "total_cost_or_revenue", "thoughts", "profit_loss"}
    flag = 0
    # Check for missing keys
    for key in required_keys:
        if key not in data:
          
           flag = 1
          #  print("Value error")
        
    if flag == 0:
      db = TinyDB('mock_journal.json')
      db.insert(json.loads(data)) 

# submit_fake()