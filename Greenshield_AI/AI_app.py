import streamlit as st
from groq import Groq

def draft_message(content, role='user'):
    return {
        "role": role,
        "content": content
    }

api_key = "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"
client = Groq(api_key=api_key)

css = """
    <style>
    /* Body Styling */
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #e8f5e9, #81c784);
        color: #2e7d32;
        margin: 0;
        padding: 0;
    }

    /* Main Container */
    .main {
        max-width: 900px;
        margin: 80px auto;
        background: #f2f2f2;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .main:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    }

    /* Header */
    h1 {
        font-size: 2.5rem;
        color: #1b5e20;
        text-align: center;
        border: solid black 2px;
        border-radius: 40px;
        background: #2f2f2f;
        margin-bottom: 20px;
        font-weight: bold;
        color: #69c227; 
    }
    h1::after {
        content: '';
        display: block;
        width: 50px;
        height: 4px;
        background: #66bb6a;
        margin: 10px auto 0;
        border-radius: 2px;
    }

    /* Input Field */
    .stTextInput label {
        font-size: 1.2rem;
        color: #2e7d32;
        font-weight: bold;
        margin-bottom: 8px;
        display: inline-block;
    }
    .stTextInput input {
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #a5d6a7;
        font-size: 1rem;
        color: #2e7d32;
        background: #f9fbe7;
        transition: border-color 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #388e3c;
        outline: none;
        box-shadow: 0 0 8px rgba(56, 142, 60, 0.3);
    }

    /* Button Styling */
    .stButton button {
        background: #66bb6a;
        color: white;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        transition: background-color 0.3s ease, transform 0.2s ease;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(102, 187, 106, 0.3);
    }
    .stButton button:hover {
        background: #388e3c;
        transform: translateY(-3px);
    }

    /* Spinner Styling */
    .stSpinner > div {
        color: #388e3c;
        animation: spin 1s infinite linear;
    }

    /* Response Box */
    .response-box {
        background: #f1f8e9;
        border-left: 4px solid #81c784;
        padding: 15px;
        border-radius: 8px;
        font-size: 1rem;
        line-height: 1.6;
        color: #2e7d32;
        margin-top: 20px;
    }

    /* Info Box */
    .stInfo {
        background: #e8f5e9;
        color: #1b5e20;
        border-radius: 8px;
        padding: 15px;
        font-size: 0.9rem;
        margin-top: 10px;
    }

    /* Warning and Error Boxes */
    .stWarning {
        background: #fffde7;
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

    /* Keyframes for Spinner Animation */
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    

    
    .h1{
    font-size: 2.5rem;
    color: neongreen;
    text-align: center;
    margin-bottom: 20px;
    font-weight: 700;
    border: solid white 2px;
    border-radius: 11px;
    margin-top: 0px;
     background-color: #36393d;
    }
    </style>
    """


html = """
<h1>🌿 GreenShield AI</h1>
<p style="text-align: center; font-size: 1.2rem;">How can GreenShield AI Help you today?</p>
"""

st.markdown(html, unsafe_allow_html=True)
st.markdown(css, unsafe_allow_html=True)

user_prompt = st.text_input("Type your prompt here pls: ", placeholder="Type your query here...")
st.markdown(
    """
    <style>
    /* Change the label color for the text input */
    div[class^="stTextInput"] label {
        font-size: 1.2rem;
        color: #4caf50; /* Your desired color */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True)


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

