import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


st.set_page_config(
    page_title="Streamlit Chat App",
    page_icon="🤖"
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "first_name" not in st.session_state:
    st.session_state.first_name = ""


prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful coding assistant created by Hippopotamus."),
        ("human","{message}")
])


tab_chat, tab_settings = st.tabs(
    ["Chat", "Settings"]
)


with tab_settings:

    st.subheader("Groq Configuration")

    api_key = st.text_input(
        "Groq API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="gsk_..."
    )

    if st.button("Save API Key"):

        if not api_key.strip():
            st.error("Please enter a valid API key.")
        else:
            st.session_state.api_key = api_key.strip()
            st.success("API key saved successfully.")

with tab_chat:

    st.header(
        "Streamlit Chat App",
        divider=True
    )

    first_name = st.text_input(
        "First Name",
        value=st.session_state.first_name
    )

    st.session_state.first_name = first_name

    
    chat_container = st.container(
        height=550,
        border=True
    )

    with chat_container:
        if not st.session_state.messages:
            with st.chat_message("assistant"):
                st.markdown(
                    f"Hello {first_name or 'there'}! How can I help you today?"
                )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    user_prompt = st.chat_input(
        "Type your message..."
    )

    if user_prompt:
        if not st.session_state.api_key:
            st.session_state.messages.append(
            {
                "role": "assistant",
                "content": "Please configure your Groq API key in the Settings tab."
            }
        )
            
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        try:

            llm = ChatGroq(
                model="groq/compound-mini",
                api_key=st.session_state.api_key
            )

            chain = prompt_template | llm

            with st.spinner("Thinking..."):
                response = chain.invoke({"message": user_prompt})

            
            st.session_state.messages.append({"role": "assistant","content": response.content})
            st.rerun()

        except Exception as e:
            st.error(
                f"Failed to generate response:\n\n{str(e)}"
            )
