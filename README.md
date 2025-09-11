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

1. **No Authentication**  - [No-Auth-README.md](no-auth/No-Auth-README.md)
2. **Username/Password Authentication (SASL/PLAIN)** - [Auth-README.md](auth/Auth-README.md)
3. **SASL_SSL Authentication with Certificates** - [SSL-Auth-README.md](sasl_ssl_auth/SSL-Auth-README.md)

Each setup includes:
- Docker Compose files for Kafka + Zookeeper
- FastAPI producer endpoints
- Streamlit UI for interactive Kafka messaging

---

## 📂 Directory Structure

```plaintext

├── auth
│ ├── Auth-README.md
│ ├── client-ui
│ │ └── kafka_ui.py
│ ├── config
│ │ ├── client.properties
│ │ └── kafka_server_jaas.conf
│ ├── docker-compose.yml
│ ├── kafka_auth.py
│ └── requirements.txt
│
├── no-auth
│ ├── client-ui
│ │ └── kafka_ui.py
│ ├── docker-compose.yml
│ ├── kafka_no_auth.py
│ ├── No-Auth-README.md
│ └── requirements.txt
│
├── README.md
│
└── sasl_ssl_auth
    ├── cert
    │ ├── ca-cert.pem
    │ ├── kafka.p12
    │ ├── keystore
    │ │ └── kafka.keystore.jks
    │ ├── script.sh
    │ └── truststore
    │     ├── ca-key
    │     └── kafka.truststore.jks
    ├── client-ui
    │ ├── kafka_streamlit_app.py
    │ └── ui_start_command.txt
    ├── config
    │ ├── consumer.properties
    │ ├── kafka.env
    │ ├── kafka_server_jaas.conf
    │ ├── producer.properties
    │ └── server.properties
    ├── docker-compose.yml
    ├── requirements.txt
    └── SSL-Auth-README.md