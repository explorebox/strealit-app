import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv


load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

st.header("Streamlit Chat App",divider=True)

llm = ChatGroq(model="groq/compound-mini")


prompt = ChatPromptTemplate([
    ("system", "You are an English to Haryanvi translator. Translate whatever the user gives you."),
    ("human", "{message}")
])

chain = prompt|llm

st.session_state.show_chat = False
st.session_state.first_name = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


tab1, tab2 = st.tabs(["Chat", "Settings"])

with tab2:
    st.write("API Option:")

    apiKey = st.text_input(label="Groq API Key")

with tab1:
    chat_container = st.container(height=500)

    with chat_container:
        with st.chat_message("assistant"):
            st.write(f"Hello, {st.session_state.first_name}")

    prompt = st.chat_input("Type your message here...")

    response = chain.stream({ "message": prompt})

    for r in response:
        st.session_state.messages.append({ "role": "assistant", "content": r.content    })

def close_sidebar():
    st.set_page_config(initial_sidebar_state="collapsed")

with st.sidebar:
    st.header("Welcome!",divider=True)

    col1, col2= st.columns(2)

    with st.form("user",border=False,width=500):

        with col1:
            first_name = st.text_input(label="First Name")
            first_name_err = st.empty()
        
        with col2:
            last_name = st.text_input(label="Last Name")
            last_name_err = st.empty()


        add_radio = st.selectbox(
            "Select Gender",
            ("Male", "Female","Mai nai bataungi!")
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            with st.spinner("Please wait..."):
                st.session_state.show_chat=True
                st.session_state.first_name=first_name

                time.sleep(5)
                close_sidebar()
