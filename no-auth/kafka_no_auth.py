from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer, Consumer, KafkaError
import uvicorn

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"  # Kafka broker address
KAFKA_GROUP_ID = "fastapi-group"
KAFKA_TOPIC = ("mock_json")

# Model for message data
class PublishMessageRequest(BaseModel):
    topic: str
    message: str


@app.post("/produce")
def produce_message(request: PublishMessageRequest):
    """Produce a message to Kafka."""
    producer_config = {
        "bootstrap.servers": KAFKA_BROKER
    }
    producer = Producer(producer_config)
    try:
        producer.produce(request.topic, value=request.message)
        producer.flush()  # Ensure all messages are sent
        return {"message": "Message produced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to produce message: {str(e)}")




@app.get("/consume")
def consume_messages():
    """Consume messages from Kafka."""
    consumer_config = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": KAFKA_GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,  # Disable auto-commit
    }

    consumer = Consumer(consumer_config)
    try:
        # Subscribe to the Kafka topic
        consumer.subscribe([KAFKA_TOPIC])
        messages = []

        # Poll for messages in a loop
        for _ in range(10):  # Poll up to 10 times before closing (adjust as needed)
            msg = consumer.poll(timeout=1.0)  # Wait for messages for up to 1 second
            if msg is None:
                continue  # No message received in this poll cycle
            if msg.error():
                # Handle Kafka-specific errors
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    raise HTTPException(status_code=500, detail=f"Kafka error: {msg.error()}")
                continue

            # Decode and append the message
            message_value = msg.value()
            if message_value is not None:
                decoded_message = message_value.decode("utf-8")  # Decode bytes to string
                messages.append(decoded_message)

        return {"messages": messages}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to consume messages: {str(e)}")

    finally:
        # Close the consumer to free up resources
        consumer.close()

# Run the FastAPI application programmatically using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)