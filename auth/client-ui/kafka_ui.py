import json
import streamlit as st
import requests

API_SERVER = "http://localhost:5000"
TOPIC_NAME = "mock_json"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.seen_messages = set()

st.set_page_config(page_title="Kafka UI", layout="wide")
st.title("Kafka Message Viewer")
st.subheader(f"📌 Topic: `{TOPIC_NAME}`")

# Message producer section
st.markdown("### 📨 Produce a Message")
with st.form("produce_form", clear_on_submit=True):
    message_text = st.text_area("Enter your message (as JSON or plain text)", height=150)
    submitted = st.form_submit_button("Send to Kafka")

    if submitted:
        if not message_text.strip():
            st.warning("Please enter a message before sending.")
        else:
            payload = {
                "topic": TOPIC_NAME,
                "message": message_text
            }
            try:
                response = requests.post(f"{API_SERVER}/produce", json=payload)
                if response.status_code == 200:
                    st.success("✅ Message sent successfully!")
                else:
                    st.error(f"❌ Failed to send message: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Error while sending: {e}")

st.divider()

# Consumer section
st.markdown("### 📥 Consume Messages")
if st.button("🔄 Refresh Messages"):
    try:
        response = requests.get(f"{API_SERVER}/consume")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            for message in messages:
                try:
                    decoded = message.decode("utf-8") if isinstance(message, bytes) else message
                    if decoded not in st.session_state.seen_messages:
                        try:
                            json_obj = json.loads(decoded)
                            st.session_state.chat_history.insert(0, json_obj)
                        except json.JSONDecodeError:
                            st.session_state.chat_history.insert(0, {"raw_text": decoded})
                        st.session_state.seen_messages.add(decoded)
                except Exception as decode_error:
                    st.warning(f"Skipped unreadable message: {decode_error}")
        else:
            st.error(f"❌ Failed to fetch messages. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error fetching messages: {e}")

# Display chat history
st.markdown("### 🧾 Message Log")
if st.session_state.chat_history:
    for idx, msg in enumerate(st.session_state.chat_history, start=1):
        st.subheader(f"Message #{idx}")
        if isinstance(msg, dict) and "raw_text" in msg:
            st.write(msg["raw_text"])
        else:
            st.json(msg)
else:
    st.info("No messages consumed yet. Click 'Refresh Messages' to fetch.")