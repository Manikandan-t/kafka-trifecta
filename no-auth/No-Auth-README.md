# 📨 Kafka Stream Viewer (FastAPI + Streamlit)

This project provides a simple local Kafka setup for producing and consuming messages using FastAPI APIs, with a Streamlit-based UI for visualizing messages from a Kafka topic.

---

## 📦 Features

- Local Kafka cluster with Docker Compose
- FastAPI-based endpoints for producing and consuming messages
- Streamlit frontend to visualize JSON Kafka messages
- Optional AES decryption support
- Message deduplication in UI

---

## 🛠️ Setup Instructions

### 1. Start Kafka and Zookeeper (Docker Compose)

Make sure Docker is running.

```bash
docker compose -f docker-compose.yml up -d
```

This spins up:
- Zookeeper on port `2181`
- Kafka broker on port `9092` (external), `29092` (Docker), `9999` (JMX)

---

### 2. Set Up Python Environment

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🚀 Running the Services

### 🔸 Start FastAPI Kafka API

```bash
python fastapi_kafka.py
```

- Runs on: `http://localhost:5000`
- Endpoints:
  - `POST /produce` → Send a message to Kafka
  - `GET /consume` → Read messages from Kafka

### 🔸 Start Streamlit UI

```bash
streamlit run kafka_ui.py
```

- Runs on: `http://localhost:8501`
- Allows refreshing and viewing Kafka messages in real time

---

## 📡 API Endpoints

### ✅ Produce Message

```http
POST /produce
Content-Type: application/json

{
  "topic": "mock_json",
  "message": "{\"referenceId\": \"REF-111\", \"documentId\": \"5354356788\"}"
}
```

> Note: `message` must be a **JSON string**, not an object.

---

### ✅ Consume Messages

```http
GET /consume
```

Returns a JSON object with a `messages` list:

```json
{
  "messages": [
    "{\"referenceId\": \"REF-111\", \"documentId\": \"5354356788\"}"
  ]
}
```

---

## 🖥️ Streamlit UI

The Streamlit app:

- Refreshes messages with a button
- Parses valid JSON responses
- Deduplicates already shown messages
- Displays raw messages (if JSON decoding fails)

---

## 🧪 Example `curl` to Send a Message

```bash
curl -X POST http://localhost:5000/produce \
  -H "Content-Type: application/json" \
  -d '{"topic": "mock_json", "message": "{\"referenceId\": \"REF-111\", \"documentId\": \"5354356788\"}"}'
```

---

## 🧼 Cleanup
To stop and remove Kafka containers:

```bash
docker compose down
```
---