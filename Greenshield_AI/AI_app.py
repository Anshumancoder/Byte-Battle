import streamlit as st
from groq import Groq

def draft_message(content, role='user'):
    return {
        "role": role,
        "content": content
    }

api_key = "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"
client = Groq(api_key=api_key)

st.markdown(
    """
    <style>
    /* General body styling */
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        color: #2e7d32;
        margin: 0;
        padding: 0;
    }

    /* Center the content container */
    .main {
        max-width: 800px;
        margin: 50px auto;
        background: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    /* Header styling */
    h1 {
        font-size: 2.5rem;
        color: #1b5e20;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 700;
    }

    /* Text input styling */
    .stTextInput label {
        font-size: 1.2rem;
        color: #388e3c;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stTextInput input {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #a5d6a7;
        font-size: 1rem;
        color: #1b5e20;
    }

    /* Button styling */
    .stButton button {
        background: #66bb6a;
        color: white;
        font-size: 1rem;
        font-color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(102, 187, 106, 0.3);
    }
    .stButton button:hover {
        background: #388e3c;
        font-color: white;
        box-shadow: 0 6px 15px rgba(56, 142, 60, 0.4);
    }

    /* Spinner styling */
    .stSpinner > div {
        color: #388e3c;
    }

    /* Response container */
    .response-box {
        background: #f1f8e9;
        border-left: 4px solid #81c784;
        padding: 15px;
        border-radius: 8px;
        font-size: 1rem;
        line-height: 1.5;
        color: #2e7d32;
        margin-top: 20px;
    }

    /* Info box styling */
    .stInfo {
        background: #c8e6c9;
        color: #1b5e20;
        border-radius: 8px;
        padding: 15px;
        font-size: 0.9rem;
        margin-top: 10px;
    }

    /* Warnings and errors */
    .stWarning {
        background: #ffecb3;
        color: #f57c00;
        border-radius: 8px;
        padding: 15px;
        font-size: 0.9rem;
        margin-top: 10px;
    }

    .stError {
        background: #ffcdd2;
        color: #c62828;
        border-radius: 8px;
        padding: 15px;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>🌿 Environmentalist Assistant</h1>", unsafe_allow_html=True)
st.write("Welcome! Enter a prompt below to interact with the assistant.")

user_prompt = st.text_input("Your Prompt:", placeholder="Type your query here...")

if st.button("Get Response"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful environmentalist assistant which can and should answer queries through "
                        "a broader perspective. Your mission is to inform the user about environmentalism and respond "
                        "to their queries in the language of their prompt. If the user query does not have much to do "
                        "with environmentalism then you should still be able to answer their query."
                    ),
                },
                draft_message(user_prompt)
            ]

            try:
                chat_completion = client.chat.completions.create(
                    temperature=1.0,
                    n=1,
                    model="mixtral-8x7b-32768",
                    max_tokens=10000,
                    messages=messages
                )

                response = chat_completion.choices[0].message.content
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

                st.info(f"Total Tokens Used: {chat_completion.usage.total_tokens}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt.")
