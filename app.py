import streamlit as st
from openai import OpenAI

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Simple AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Simple AI Agent")
st.caption("Workflow: User → LLM (Reasoning) → Response")

# ---------------------------------
# Session State
# ---------------------------------
if "answer" not in st.session_state:
    st.session_state.answer = ""

# ---------------------------------
# Sidebar
# ---------------------------------
st.sidebar.header("Settings")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

model = st.sidebar.selectbox(
    "Model",
    [
        "gpt-4.1-mini",
        "gpt-4.1",
        "gpt-5-mini"
    ]
)

# ---------------------------------
# User Input
# ---------------------------------
user_query = st.text_area(
    "Ask your question",
    placeholder="Example: Explain Artificial Intelligence"
)

# ---------------------------------
# Generate Response
# ---------------------------------
if st.button("Generate Response"):

    if api_key == "":
        st.error("Please enter your OpenAI API Key.")
        st.stop()

    if user_query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    client = OpenAI(api_key=api_key)

    with st.spinner("Thinking..."):

        result = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )

        st.session_state.answer = result.output_text

# ---------------------------------
# Display Workflow
# ---------------------------------
if st.session_state.answer:

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👤 User")
        st.info(user_query)

    with col2:
        st.subheader("🧠 LLM")
        st.success("Reasoning Completed")

    with col3:
        st.subheader("🤖 Response")
        st.success("Answer Generated")

    st.divider()

    st.subheader("Workflow")

    st.code(
"""User
   │
   ▼
LLM (Reasoning)
   │
   ▼
Response"""
    )

    st.divider()

    st.subheader("Final Answer")

    st.write(st.session_state.answer)
