import streamlit as st
from transformers import pipeline

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Simple AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Simple AI Agent")
st.caption("Workflow: User → LLM (Reasoning) → Response")

# -----------------------------------
# Load Model
# -----------------------------------
@st.cache_resource
def load_llm():
    generator = pipeline(
        "text-generation",
        model="distilgpt2"
    )
    return generator

llm = load_llm()

# -----------------------------------
# User Input
# -----------------------------------
user_query = st.text_area(
    "Ask anything",
    placeholder="Example: Explain Artificial Intelligence"
)

# -----------------------------------
# Generate Response
# -----------------------------------
if st.button("Generate Response"):

    if user_query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Thinking..."):

        prompt = f"""
You are a helpful AI Assistant.

User:
{user_query}

Think carefully before answering.

Answer:
"""

        output = llm(
            prompt,
            max_new_tokens=120,
            temperature=0.7,
            do_sample=True
        )

        response = output[0]["generated_text"]

        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()

    # -----------------------------------
    # Display Workflow
    # -----------------------------------

    st.success("Response Generated!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👤 User")
        st.info(user_query)

    with col2:
        st.subheader("🧠 LLM Reasoning")
        st.write("Analyzing the prompt...")
        st.progress(100)

    with col3:
        st.subheader("🤖 Response")
        st.success(response)

    st.divider()

    st.subheader("Workflow")

    st.markdown("""
```text
User
   │
   ▼
LLM (Reasoning)
   │
   ▼
Response
""")
st.divider()

st.subheader("Final Answer")

st.write(response)
