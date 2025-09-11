import io
import uuid

import streamlit as st
import pandas as pd
from confluent_kafka import Consumer, KafkaException, OFFSET_BEGINNING, KafkaError
import os
import json

st.set_page_config(layout="wide")
st.title("Kafka Data Viewer")

st.write("""
This application connects to a Kafka topic, consumes a specified number of messages,
and displays them.
""")

# --- Kafka Configuration ---
# You can get these from environment variables, a config file, or directly here
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "example.kafka.com:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "mock_json_topic") # Change to your topic
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "springbootapi-group")

# For SASL_SSL PLAIN
# Ensure these paths are correct relative to where you run the Streamlit app
# You might need to copy kafka.truststore.jks to a location accessible by the Streamlit app
CA_LOCATION = os.getenv("KAFKA_CA_LOCATION", "../cert/ca-cert.pem") # This is the crucial change

# Define JAAS config directly or load from a file
SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME", "user")
SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD", "bitnami")


st.sidebar.header("Kafka Connection Settings")
broker_input = st.sidebar.text_input("Kafka Broker (Host:Port)", KAFKA_BROKER)
topic_input = st.sidebar.text_input("Kafka Topic", KAFKA_TOPIC)
group_id_input = st.sidebar.text_input("Consumer Group ID", f"viewer-{uuid.uuid4()}")
num_messages_to_consume = st.sidebar.number_input("Number of Messages to Consume", min_value=1, value=10, step=1)
# Add an option to start from beginning of topic
start_from_beginning = st.sidebar.checkbox("Start from beginning (resets offset)", False)


# Function to create Kafka Consumer
@st.cache_resource
def get_kafka_consumer(broker, group_id):
    try:
        conf = {
            'bootstrap.servers': broker,
            'group.id': group_id,
            'auto.offset.reset': 'earliest', # Important for initial consumption
            'security.protocol': 'SASL_SSL',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': SASL_USERNAME,
            'sasl.password': SASL_PASSWORD,
            'ssl.endpoint.identification.algorithm': 'none', #Try skipping verification (not recommended long term)
            'ssl.ca.location': CA_LOCATION,
            'session.timeout.ms': 10000, # Increased session timeout
            'heartbeat.interval.ms': 3000,
            'max.poll.interval.ms': 10000,
            'debug': 'security,broker,protocol'
        }
        consumer = Consumer(conf)
        return consumer
    except Exception as e:
        st.error(f"Error initializing Kafka Consumer: {e}")
        st.stop()
        return None

# Initialize Kafka Consumer
consumer = get_kafka_consumer(broker_input, group_id_input)

if consumer:
    if st.button(f"Consume {num_messages_to_consume} Messages"):
        st.info(f"Connecting to Kafka broker: {broker_input}, topic: {topic_input}...")
        try:
            consumer.subscribe([topic_input])

            if start_from_beginning:
                st.warning("Resetting consumer offset to beginning of all partitions...")
                from confluent_kafka import TopicPartition, OFFSET_BEGINNING

                metadata = consumer.list_topics(topic_input, timeout=10)
                partitions = metadata.topics[topic_input].partitions
                topic_partitions = [TopicPartition(topic_input, p, OFFSET_BEGINNING) for p in partitions]
                consumer.assign(topic_partitions)

            messages = []
            message_count = 0
            timeout_ms = 1000 # Max time to wait for a message in milliseconds

            progress_bar = st.progress(0)
            status_text = st.empty()

            while message_count < num_messages_to_consume:
                msg = consumer.poll(timeout_ms / 1000.0) # poll expects seconds

                if msg is None:
                    status_text.text(f"Waiting for messages... ({message_count}/{num_messages_to_consume})")
                    if message_count == 0 and num_messages_to_consume > 0:
                        st.warning(f"No messages received in {timeout_ms/1000.0} seconds. Trying again...")
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event - not an error
                        status_text.text(f"Reached end of partition {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                        continue
                    else:
                        st.error(f"Kafka error: {msg.error()}")
                        break

                # Process the message
                key = msg.key().decode('utf-8') if msg.key() else None
                value = msg.value().decode('utf-8') if msg.value() else None
                timestamp = pd.to_datetime(msg.timestamp()[1], unit='ms') if msg.timestamp() else None

                # Assuming messages are JSON, parse them
                try:
                    parsed_value = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    parsed_value = value # Keep as raw string if not JSON

                messages.append({
                    "Timestamp": timestamp,
                    "Topic": msg.topic(),
                    "Partition": msg.partition(),
                    "Offset": msg.offset(),
                    "Key": key,
                    "Value": parsed_value
                })
                message_count += 1
                progress_bar.progress(message_count / num_messages_to_consume)
                status_text.text(f"Consumed {message_count}/{num_messages_to_consume} messages.")

            if messages:
                df = pd.DataFrame(messages)
                st.subheader("Consumed Kafka Messages")
                st.dataframe(df)

                st.subheader("Data Information")
                buffer = io.StringIO()
                df.info(buf=buffer)
                s = buffer.getvalue()
                st.text(s)

                st.subheader("Message Values (Raw)")
                # Display raw JSON values nicely if applicable
                for msg_val in df['Value']:
                    st.json(msg_val) if isinstance(msg_val, dict) else st.write(msg_val)
            else:
                st.info("No messages consumed.")

        except KafkaException as ke:
            st.error(f"Kafka connection error: {ke}")
            st.info("Please ensure the Kafka broker is running and accessible, and your connection settings are correct.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
        finally:
            pass
else:
    st.error("Kafka Consumer could not be initialized. Check console for errors.")

st.info("Remember to produce some messages to your Kafka topic to see data here!")