# Kafka SSL Setup with Docker and Streamlit UI

This guide walks you through the process of:

- Generating truststore and keystore files
- Running a Kafka broker over SSL with Docker
- Producing and consuming Kafka messages
- Converting `.jks` to `.pem` for use with Python (Streamlit UI)

---

## 🚀 Step-by-Step Instructions

### 1. Generate Truststore and Keystore

## 🔐 SSL Certificate Script (sasl-ssl-auth/script.sh)

This script automates the creation of **SSL keystores and truststores** for Kafka brokers and clients. It is required for enabling **SASL_SSL** authentication, which encrypts communication and verifies identities using X.509 certificates.

### 🛠️ What Does the Script Do?

The script guides you through:

1. **Truststore generation** (if needed):
   - Creates a CA (Certificate Authority) private key and certificate
   - Imports the CA certificate into a new truststore

2. **Keystore generation**:
   - Creates a keystore containing a key pair (private key + self-signed cert)
   - Generates a **certificate signing request (CSR)** from the keystore
   - Signs the CSR with the **CA private key** created earlier
   - Imports the signed certificate and CA into the keystore

3. **Cleanup** (optional):
   - Prompts to delete intermediate files like CSR and signed cert

### 📁 Output Structure

- `keystore/kafka.keystore.jks` — used by Kafka broker/client for SSL
- `truststore/kafka.truststore.jks` — used to trust the CA
- Intermediate files (can be deleted after setup):
  - `ca-cert`, `cert-file`, `cert-signed`, `ca-cert.srl`

### 📌 Requirements

- `openssl`
- `keytool` (comes with Java JDK)

Make sure these are installed and available in your system PATH.

### 🚀 Running the Script
Use password: 123456

```bash
chmod +x script.sh
./script.sh
```


---

### 2. Create Docker Network

Create a Docker network for Kafka:

```bash
docker network create kafka
```

---

### 3. Start Kafka Using Docker Compose

Run the following command to start Kafka:

```bash
docker compose -f docker-compose.yml up -d
```

---

### 4. Verify Kafka Logs

Make sure the Kafka broker is running properly. Look for messages like:

```text
example.kafka.com  | [2025-07-14 21:30:00,685] INFO [BrokerServer id=0] Finished waiting for the broker to be unfenced (kafka.server.BrokerServer)
example.kafka.com  | [2025-07-14 21:30:00,686] INFO authorizerStart completed for endpoint SASL_SSL. Endpoint is now READY. (org.apache.kafka.server.network.EndpointReadyFutures)
```

---

### 5. Add Host Mapping

Edit your `/etc/hosts` file and add:

```text
172.20.0.2 example.kafka.com
```

---

## 🧪 Produce and Consume Kafka Messages

### Enter the Kafka Container

```bash
docker exec -it $(docker ps -qf "ancestor=bitnami/kafka") bash
```

### Create a Kafka Topic

```bash
kafka-topics.sh \
  --create \
  --bootstrap-server example.kafka.com:9092 \
  --command-config /opt/bitnami/kafka/config/producer.properties \
  --replication-factor 1 \
  --partitions 1 \
  --topic mock_json_topic
```

### Produce Messages to the Topic

```bash
kafka-console-producer.sh \
  --bootstrap-server example.kafka.com:9092 \
  --producer.config /opt/bitnami/kafka/config/producer.properties \
  --topic mock_json_topic
```

### Consume Messages from the Topic

```bash
kafka-console-consumer.sh \
  --bootstrap-server example.kafka.com:9092 \
  --consumer.config /opt/bitnami/kafka/config/consumer.properties \
  --topic mock_json_topic \
  --from-beginning
```

---

## 📦 Using Python / Streamlit UI with SSL

Python (e.g., Streamlit) requires `.pem` files instead of `.jks`. Here's how to convert the truststore:

### Step 1: Export the CA Certificate from the JKS Truststore

```bash
keytool -exportcert \
  -alias caroot \
  -keystore truststore/kafka.truststore.jks \
  -storepass 123456 \
  -rfc \
  -file truststore/ca-cert.pem
```

### Step 2: Run the Streamlit App

```bash
streamlit run kafka_streamlit_app.py
```

---

## ✅ Summary

- Secure Kafka setup using SSL
- Dockerized for isolation and ease of deployment
- Tools provided for creating topics, producing, and consuming messages
- Support for Python clients (with `.pem` certs)

---

## 📄 Notes

- Ensure all hostnames and ports match your environment
- Adjust passwords and aliases as needed for your security policies
