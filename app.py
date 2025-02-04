import os
import streamlit as st
from openai import AzureOpenAI

# Set up Azure OpenAI credentials from environment variables
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Initialize Azure OpenAI Service client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

# Streamlit App Layout
st.title("LetsAI copilot")

# Initialize session state for messages if not already present
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to call Azure OpenAI model
def azure_openai_chat(messages):
    try:
        completion = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat history in a chat-like format
for message in st.session_state['messages']:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["content"])

# Chat input field
prompt = st.chat_input("Say something")

if prompt:
    # Display user message
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare context: last 5 messages + system prompt
    context = [{"role": "system", "content": "You are LetsAI internal chatbot made for internal coding purposes"}]
    last_5_messages = st.session_state['messages'][-5:]  # Keep only the last 5 messages
    context.extend(last_5_messages)

    # Get AI response
    response = azure_openai_chat(context)

    # Display assistant message
    st.session_state['messages'].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
