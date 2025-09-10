# kafka-trifecta
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
```
