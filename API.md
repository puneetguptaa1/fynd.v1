# Fynd API Documentation

## Overview

The Fynd API provides endpoints to process natural language queries and return restaurant recommendations based on user criteria.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

Check if the API is running.

**Request:**
```
GET /
```

**Response:**
```json
{
  "status": "ok",
  "message": "Fynd API is running"
}
```

### Process Query

Send a dining query and receive a response.

**Request:**
```
POST /query
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "query": "Find me a romantic Thai place in NYC that stays open past 11 p.m.",
  "stream": false
}
```

**Response:**
```json
{
  "response": "Based on your request for a romantic Thai place in NYC that stays open past 11 p.m., here are some options...",
  "metadata": null
}
```

### Stream Query

Stream a dining query response.

**Request:**
```
POST /query/stream
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "query": "Find me a romantic Thai place in NYC that stays open past 11 p.m.",
  "stream": true
}
```

**Response:**

The response is a server-sent event stream with chunks of the generated text:

```
data: Based
data:  on
data:  your
data:  request
...
data: [DONE]
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - The request was successful
- `400 Bad Request` - The request was invalid
- `500 Internal Server Error` - An error occurred on the server

Error responses include a detail message:

```json
{
  "detail": "Error processing query: Connection error"
}
```

## Usage Example

Here's an example using Python and the requests library:

```python
import requests

# Regular query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "Find me a romantic Italian place in NYC that stays open past 11 p.m.",
        "stream": False
    }
)
print(response.json())

# Streaming query
with requests.post(
    "http://localhost:8000/query/stream",
    json={
        "query": "Find me a casual Mexican restaurant in San Francisco with good margaritas.",
        "stream": True
    },
    stream=True
) as response:
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
``` 