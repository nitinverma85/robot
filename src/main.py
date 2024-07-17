import ollama
import streamlit as st


# configuring streamlit page settings
st.set_page_config(
    page_title="HelloFresh - Ask Data Questions",
    # page_icon="💬",
    layout="centered"
)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("HelloFresh - Ask Data Questions")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Ask a data question")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "system",
             "content": "You are a SQL expert, so only reply with a Spark SQL query. Please reply only with SQL code and remove everything else."},
            *st.session_state.chat_history
        ]
    )

    # Generate model response
    assistant_response = response["message"]["content"]
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
