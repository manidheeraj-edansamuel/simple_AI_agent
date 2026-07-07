import streamlit as st
from openai import OpenAI

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="Simple AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Simple AI Agent")
st.caption("Workflow: User → NVIDIA LLM → Response")

# ----------------------------------
# NVIDIA Client
# ----------------------------------

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["NVIDIA_API_KEY"]
)

# ----------------------------------
# User Input
# ----------------------------------

question = st.text_area(
    "Ask anything",
    placeholder="Explain Artificial Intelligence"
)

# ----------------------------------
# Button
# ----------------------------------

if st.button("Generate Response"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Thinking..."):

        completion = client.chat.completions.create(

            model="meta/llama-3.1-8b-instruct",

            messages=[
                {
                    "role":"system",
                    "content":"You are a helpful AI assistant."
                },
                {
                    "role":"user",
                    "content":question
                }
            ],

            temperature=0.5,
            max_tokens=512

        )

        answer = completion.choices[0].message.content

    st.success("Response Generated!")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("👤 User")
        st.info(question)

    with c2:
        st.subheader("🧠 LLM")
        st.write("Reasoning...")
        st.progress(100)

    with c3:
        st.subheader("🤖 Response")
        st.success(answer)

    st.divider()

    st.subheader("Workflow")

    st.code("""
User
  │
  ▼
NVIDIA LLM
  │
  ▼
Response
""")

    st.divider()

    st.subheader("Final Response")

    st.write(answer)
