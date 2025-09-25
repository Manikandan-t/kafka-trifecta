# Kafka Trifecta: Secure Kafka Setup with Multiple Authentication Methods

## 🧠 What is Kafka?

[Apache Kafka](https://kafka.apache.org/) is a distributed event streaming platform used for building real-time data pipelines and streaming applications. It enables the publishing, subscription, storage, and processing of streams of records in a fault-tolerant and scalable way.

Kafka works on a **producer-consumer** model:
- **Producers** send data to Kafka **topics**
- **Consumers** subscribe to those topics and process the data

## 🐘 What is Zookeeper?

Kafka uses **Zookeeper** to manage:
- Broker metadata
- Leader election for partitions
- Configuration synchronization across brokers

> While modern Kafka versions support a KRaft (Kafka Raft) mode that eliminates the need for Zookeeper, it's still commonly used in development and legacy setups.

---

## 📁 Project Structure

This repository demonstrates how to set up and run Kafka locally with three different security configurations:

```
kafka-trifecta/
├── auth/                # SASL/PLAIN Authentication
│   ├── Auth-README.md
│   ├── client-ui/
│   │   └── kafka_ui.py
│   ├── config/
│   │   ├── client.properties
│   │   └── kafka_server_jaas.conf
│   ├── docker-compose.yml
│   ├── kafka_auth.py
│   └── requirements.txt
│
├── no-auth/             # No Authentication
│   ├── No-Auth-README.md
│   ├── client-ui/
│   │   └── kafka_ui.py
│   ├── docker-compose.yml
│   ├── kafka_no_auth.py
│   └── requirements.txt
│
└── sasl_ssl_auth/       # SASL_SSL Authentication with Certificates
    ├── SSL-Auth-README.md
    ├── client-ui/
    │   ├── kafka_streamlit_app.py
    │   └── ui_start_command.txt
    ├── config/
    │   ├── consumer.properties
    │   ├── kafka.env
    │   ├── kafka_server_jaas.conf
    │   ├── producer.properties
    │   └── server.properties
    ├── cert/
    │   ├── ca-cert.pem
    │   ├── kafka.p12
    │   ├── keystore/
    │   │   └── kafka.keystore.jks
    │   ├── script.sh
    │   └── truststore/
    │       ├── ca-key
    │       └── kafka.truststore.jks
    ├── docker-compose.yml
    └── requirements.txt
```

---

## 🔐 Kafka Trifecta Overview

This repository demonstrates how to set up and run Kafka locally with three different security configurations:

1. **No Authentication** - [No-Auth-README.md](no-auth/No-Auth-README.md)
2. **Username/Password Authentication (SASL/PLAIN)** - [Auth-README.md](auth/Auth-README.md)
3. **SASL_SSL Authentication with Certificates** - [SSL-Auth-README.md](sasl_ssl_auth/SSL-Auth-README.md)

Each setup includes:
- Docker Compose files for Kafka + Zookeeper
- FastAPI producer endpoints
- Streamlit UI for interactive Kafka messaging

---

## 🧪 Setup Instructions

### Prerequisites
- Docker installed and running
- Docker Compose installed (v2+ recommended)
- Java JDK (for certificate generation)
- Python 3.7+ with pip
- OpenSSL (for certificate generation)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manikandan-t/kafka-trifecta.git
cd kafka-trifecta
```

### Step 2: Choose Your Configuration

You can choose to set up one of the three configurations:

1. **No Authentication**
2. **SASL/PLAIN Authentication**
3. **SASL_SSL Authentication with Certificates**

Let's go through each setup in detail.

---

## 🔐 1. SASL/PLAIN Authentication Setup

### 🛠️ Setup Instructions

#### 1. Start Kafka with Authentication
```bash
docker compose -f auth/docker-compose.yml up -d
```

This will start:
- Zookeeper on port `2181`
- Authenticated Kafka broker on port `9092`

#### 2. Create a Kafka Topic
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --topic mock_json --create \
  --partitions 1 --replication-factor 1 \
  --command-config auth/config/client.properties
```

#### 3. Set Up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r auth/requirements.txt
```

#### 4. Run the Services
```bash
# Start FastAPI Kafka Auth API
python auth/kafka_auth.py

# Start Streamlit UI
streamlit run auth/client-ui/kafka_ui.py
```

### 📡 API Endpoints
- **POST /produce**: Send a message to Kafka
  ```http
  POST /produce
  Content-Type: application/json
  {
    "topic": "mock_json",
    "message": "{\"referenceId\": \"AUTH-001\", \"documentId\": \"1234567890\"}"
  }
  ```
  
- **GET /consume**: Read messages from Kafka
  ```http
  GET /consume
  ```
  Returns:
  ```json
  {
    "messages": [
      "{\"referenceId\": \"AUTH-001\", \"documentId\": \"1234567890\"}"
    ]
  }
  ```

### 🖥️ Streamlit UI Features
- Refresh messages with a button
- Parse and display valid JSON messages
- Deduplicate already shown messages
- Display raw messages if JSON decoding fails

---

## 📦 2. No Authentication Setup

### 🛠️ Setup Instructions

#### 1. Start Kafka Without Authentication
```bash
docker compose -f no-auth/docker-compose.yml up -d
```

This will start:
- Zookeeper on port `2181`
- Kafka broker on port `9092` (external), `29092` (Docker), `9999` (JMX)

#### 2. Create a Kafka Topic
```bash
kafka-topics --create --topic mock_json --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

#### 3. Set Up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r no-auth/requirements.txt
```

#### 4. Run the Services
```bash
# Start FastAPI Kafka API
python no-auth/kafka_no_auth.py

# Start Streamlit UI
streamlit run no-auth/client-ui/kafka_ui.py
```

### 📡 API Endpoints
- **POST /produce**: Send a message to Kafka
  ```http
  POST /produce
  Content-Type: application/json
  {
    "topic": "mock_json",
    "message": "{\"referenceId\": \"REF-111\", \"documentId\": \"5354356788\"}"
  }
  ```
  
- **GET /consume**: Read messages from Kafka
  ```http
  GET /consume
  ```
  Returns:
  ```json
  {
    "messages": [
      "{\"referenceId\": \"REF-111\", \"documentId\": \"5354356788\"}"
    ]
  }
  ```

### 🖥️ Streamlit UI Features
- Refresh messages with a button
- Parse and display valid JSON messages
- Deduplicate already shown messages
- Display raw messages if JSON decoding fails

---

## 🔐 3. SASL_SSL Authentication with Certificates Setup

### 🛠️ Setup Instructions

#### 1. Generate SSL Certificates
First, you need to generate the SSL certificates using the provided script:

```bash
cd sasl_ssl_auth/cert
chmod +x script.sh
./script.sh
```

This script will:
- Create a CA certificate and private key
- Generate a keystore with a key pair and self-signed certificate
- Sign the certificate with the CA
- Create truststore with the CA certificate

#### 2. Create Docker Network
```bash
docker network create kafka
```

#### 3. Start Kafka Using Docker Compose
```bash
docker compose -f sasl_ssl_auth/docker-compose.yml up -d
```

#### 4. Verify Kafka Logs
Check the logs to ensure Kafka is running properly:
```bash
docker logs example.kafka.com
```

You should see messages indicating the broker is ready.

#### 5. Add Host Mapping
Edit your `/etc/hosts` file and add:
```text
172.20.0.2 example.kafka.com
```

#### 6. Create a Kafka Topic
```bash
kafka-topics.sh \
  --create \
  --bootstrap-server example.kafka.com:9092 \
  --command-config sasl_ssl_auth/config/producer.properties \
  --replication-factor 1 \
  --partitions 1 \
  --topic mock_json_topic
```

#### 7. Set Up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r sasl_ssl_auth/requirements.txt
```

#### 8. Run the Streamlit UI
```bash
export KAFKA_BROKER="example.kafka.com:9092"
export KAFKA_TOPIC="mock_json_topic"
export KAFKA_SASL_USERNAME="user"
export KAFKA_SASL_PASSWORD="bitnami"
export KAFKA_CA_LOCATION="../cert/ca-cert.pem"
streamlit run sasl_ssl_auth/client-ui/kafka_streamlit_app.py
```

### 📡 API Endpoints
The FastAPI endpoints are not used in this configuration. Instead, you interact with Kafka directly through the Streamlit UI or CLI tools.

### 🖥️ Streamlit UI Features
- Connect to Kafka broker with SSL authentication
- Consume messages from a specified topic
- View message details including timestamp, partition, offset, and value
- Display raw JSON messages or plain text
- Configure connection settings via sidebar

---

## 📋 CLI Commands

### Listing Topics
```bash
# For no-auth configuration
kafka-topics --list --bootstrap-server localhost:9092

# For auth configuration
kafka-topics.sh --list --bootstrap-server localhost:9092 --command-config auth/config/client.properties

# For SASL_SSL configuration
kafka-topics.sh --list --bootstrap-server example.kafka.com:9092 --command-config sasl_ssl_auth/config/consumer.properties
```

### Publishing a Message
```bash
# For no-auth configuration
kafka-console-producer.sh --topic mock_json --bootstrap-server localhost:9092

# For auth configuration
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic mock_json --producer.config auth/config/client.properties

# For SASL_SSL configuration
kafka-console-producer.sh --topic mock_json_topic --bootstrap-server example.kafka.com:9092 --producer.config sasl_ssl_auth/config/producer.properties
```

### Consuming Messages
```bash
# For no-auth configuration
kafka-console-consumer.sh --topic mock_json --bootstrap-server localhost:9092 --from-beginning

# For auth configuration
kafka-console-consumer.sh --topic mock_json --bootstrap-server localhost:9092 --consumer.config auth/config/client.properties --from-beginning

# For SASL_SSL configuration
kafka-console-consumer.sh --topic mock_json_topic --bootstrap-server example.kafka.com:9092 --consumer.config sasl_ssl_auth/config/consumer.properties --from-beginning
```

---

## 🧪 Cleanup

To stop and remove all containers:

```bash
# For no-auth configuration
docker compose -f no-auth/docker-compose.yml down

# For auth configuration
docker compose -f auth/docker-compose.yml down

# For SASL_SSL configuration
docker compose -f sasl_ssl_auth/docker-compose.yml down
```

---

## 📌 Notes

1. **Certificate Management**: For the SASL_SSL configuration, the `ca-cert.pem` file is required for the Streamlit UI to trust the CA. Ensure this file is accessible when running the UI.

2. **Docker Network**: The SASL_SSL configuration requires a Docker network named `kafka` to be created before starting the containers.

3. **Host Mapping**: The `/etc/hosts` entry is necessary for the SASL_SSL configuration to resolve the hostname correctly.

4. **Security Best Practices**: 
   - Never use the provided default credentials (`deploy/deploy@123`, `user/bitnami`) in production
   - Always rotate certificates and credentials regularly
   - Use separate certificates for different environments (development, staging, production)

5. **Troubleshooting Tips**:
   - If you encounter connection issues, check Kafka logs with `docker logs example.kafka.com`
   - Verify that the `ssl.ca.location` is correctly pointing to the CA certificate
   - Ensure all required ports are open (9092 for SASL_SSL, 9092 for no-auth, 9092 for auth)

---

## 🙏 Acknowledgements

This project was inspired by the need to have a simple, secure way to test and develop with Kafka locally.
