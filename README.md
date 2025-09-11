# kafka-trifecta

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

## 🔐 kafka-trifecta Overview

This repository demonstrates how to set up and run Kafka locally with three different security configurations:

1. **No Authentication**
2. **Username/Password Authentication (SASL/PLAIN)**
3. **SASL_SSL Authentication with Certificates**

Each setup includes:
- Docker Compose files for Kafka + Zookeeper
- FastAPI producer endpoints
- Streamlit UI for interactive Kafka messaging

---

## 📂 Directory Structure

```plaintext
├── auth
│   ├── client-ui
│   │   └── kafka_ui.py
│   ├── config
│   │   ├── client.properties
│   │   └── kafka_server_jaas.conf
│   ├── Auth-README.md
│   ├── docker-compose.yml
│   ├── kafka_auth.py
│   └── requirements.txt
│
├── no-auth
│   ├── client-ui
│   │   └── kafka_ui.py
│   ├── docker-compose.yml
│   ├── kafka_no_auth.py
│   ├── No-Auth-README.md
│   └── requirements.txt
│
├── sasl-ssl-auth
│   ├── script.sh
│   ├── docker-compose.yml
│   ├── kafka_ssl.py
│   └── client-ui
│       ├── kafka_streamlit_app.py
│       └── requirements.txt
└── README.md