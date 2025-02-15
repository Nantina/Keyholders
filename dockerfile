FROM python:3.8-alpine

WORKDIR /app
COPY . /app

RUN pip install flask openai requests yfinance talib

CMD ["python", "app.py"]


FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
