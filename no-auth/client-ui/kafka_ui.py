import json
import streamlit as st
import requests

API_SERVER = "http://localhost:5000"
TOPIC_NAME = "mock_json"  # Kafka topic

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List to store messages
    st.session_state.seen_messages = set()  # Set for deduplication

# Streamlit UI
st.title("Kafka Message Viewer")
st.header(f"Topic: {TOPIC_NAME}")

# Refresh button
if st.button("Refresh Messages"):
    try:
        # Call the FastAPI endpoint
        response = requests.get(f"{API_SERVER}/consume")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])

            # Prepend new messages to chat history
            for message in messages:
                try:
                    response_json = json.loads(message)
                    if message not in st.session_state.seen_messages:
                        st.session_state.chat_history.insert(0, response_json)
                        st.session_state.seen_messages.add(message)
                except json.JSONDecodeError:
                    st.warning("Skipped invalid JSON message: " + message)

        else:
            st.error(f"Failed to fetch messages. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching messages: {e}")

# Display the current chat history as JSON nodes
for idx, response in enumerate(st.session_state.chat_history, start=1):
    # If this is a raw string fallback
    if "raw_text" in response:
        st.subheader(f"Message #{idx} (Raw Text)")
        st.write(response["raw_text"])
    else:
        st.subheader(f"Message #{idx}")
        st.json(response) # Display each response as a JSON node