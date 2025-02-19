FROM python:3.10-alpine

# # Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True

# Install required system dependencies
RUN apk add --no-cache g++ gcc libffi-dev musl-dev python3-dev cmake \
    linux-headers libstdc++ bash

WORKDIR /app
COPY requirements.txt .

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
