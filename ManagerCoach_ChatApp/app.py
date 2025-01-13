import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import openai

load_dotenv()
import secret
key = secret.openai_api_key
if key is None:
    key = os.getenv("OPENAI-API-KEY")

client = OpenAI(
    api_key = key
)
with open(r"C:\Users\Aditya Kumar\PycharmProjects\ManagerCoach_ChatApp\ManagerCoach_ChatApp\prompt.txt",'r') as f:
    system_prompt = f.read()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# OpenAI API
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response.choices[0].message
    messages.append(bot_message)

    st.session_state["user_input"] = ""



st.title("Manager Coach")
st.write("🤖 Hello! Feel free to ask me anything related to your managerial concerns.")

if st.button("Clear Session State"):
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]
    st.session_state["user_input"] = ""  # Clear user input field as well
    st.write("Session state cleared!")

user_input = st.text_input("Please write your query.", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):
        try:
            speaker = "🙂"
            if message.role == "assistant":  # Access role using dot notation
                speaker = "🤖"
            st.write(speaker + ": " + message.content)  # Access content using dot notation
        except AttributeError:
            # If an error occurs (i.e., the message is not of the expected type), skip it
            speaker = "🙂"
            if message["role"] == "assistant":  # Access role using dot notation
                speaker = "🤖"
            st.write(speaker + ": " + message["content"])