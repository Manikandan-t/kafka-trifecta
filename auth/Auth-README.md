# 🔐 Kafka Stream Viewer (With Authentication)

This version of the project adds authentication to your local Kafka setup while maintaining the same FastAPI and Streamlit-based interface for producing, consuming, and visualizing messages.

---

## 🔐 Features (Auth Version)

- Kafka & Zookeeper with SASL/PLAIN authentication via Docker Compose
- FastAPI endpoints with client authentication
- Streamlit UI with no change — connects via authenticated API
- Uses `client.properties` for CLI tools
- Compatible with Kafka CLI for admin tasks

---

## 🛠️ Setup Instructions

### 1. Start Kafka and Zookeeper with Authentication

Ensure Docker is running, then start Kafka with SASL/PLAIN authentication enabled:

```bash
docker compose -f docker-compose.yml up -d
```

This setup includes:
- Zookeeper on port `2181`
- Authenticated Kafka broker on port `9092`

---

### 2. Access the Kafka Container

To navigate into the Kafka Docker container:

```bash
docker exec -it kafka bash
```

---

### 3. Create a Kafka Topic with Authentication

Use the Kafka CLI tool with the `client.properties` file:

```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --topic mock_json --create \
  --partitions 1 --replication-factor 1 \
  --command-config client.properties
```

---

### 4. Set Up Python Environment

Install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🚀 Running the Services (With Auth)

### 🔸 Start FastAPI Kafka Auth API

```bash
python kafka_auth.py
```

- Runs on: `http://localhost:5000`
- Handles Kafka authentication using `client.properties` or equivalent config

### 📄 Including Swagger Docs Access

FastAPI provides automatic API documentation at:

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

### 🔸 Start Streamlit UI

```bash
streamlit run kafka_ui.py
```

- Runs on: `http://localhost:8501`
- Displays messages from Kafka via authenticated API

---

## 📡 API Endpoints (Same as Before)

### ✅ Produce Message

```http
POST /produce
Content-Type: application/json

{
  "topic": "mock_json",
  "message": "{\"referenceId\": \"AUTH-001\", \"documentId\": \"1234567890\"}"
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
    "{\"referenceId\": \"AUTH-001\", \"documentId\": \"1234567890\"}"
  ]
}
```

---

## 🖥️ Streamlit UI

The Streamlit app:
- Uses the same interface as the non-auth version
- Interacts with FastAPI backend, which handles authentication
- Provides support for both produce and consume message
- Parses and deduplicates messages

---

## 🧪 CLI Commands (Authenticated)

### 📄 Listing Topics with Authentication

```bash
kafka-topics.sh --list --bootstrap-server localhost:9092 \
  --command-config client.properties
```

---

### ✉️ Publishing a Message to Producer with Authentication

```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic mock_json \
  --producer.config client.properties
```

---

### 📥 Reading Messages from Consumer with Authentication

```bash
kafka-console-consumer.sh --topic mock_json \
  --bootstrap-server localhost:9092 \
  --consumer.config client.properties \
  --from-beginning
```

> Optional: Add `--max-messages 1` to read a single message.

---

## 🧼 Cleanup

To stop and remove authenticated Kafka containers:

```bash
docker compose -f docker-compose.yml down
```

---