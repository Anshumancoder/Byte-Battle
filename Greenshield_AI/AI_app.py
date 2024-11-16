import google.generativeai as genai
import streamlit as st

genai.configure(api_key="AIzaSyBU0NzJcqET0jZRS86bFwA0DXpPJwKjgAQ")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=[
        "You are a helpful environmentalist assistant which can and should answer to queries through a broader perpective.",
        "Your mission is to inform the user about environmentalism and respond to their queries in the language of their prompt."
        "If the user query does not have much to do with environmentalism then you should still be able to answer their query."
    ]
)

css = """
<style>
body {
    background-color: #e0f7fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    margin: 0;
    padding: 0;
}

h1 {
    color: #00796b;
    text-align: center;
    margin-top: 0px;
    font-size: 3.5em;
    letter-spacing: 1px;
}

p {
    text-align: center;
    font-size: 1.2em;
    margin-bottom: 40px;
}

#user-input {
    width: 100%;
    padding: 15px;
    font-size: 1.1em;
    margin-bottom: 20px;
    border: 2px solid #00796b;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

#user-input:focus {
    border-color: #004d40;
    outline: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

#response-box {
    background-color: #474747;
    padding: 25px;
    border-radius: 10px;
    margin-top: 20px;
    border: 1px solid #004d40;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

#response-box:hover {
    transform: translateY(-5px);
}

strong {
    color: linear-gradient(to right, white, black);
    font-weight: bold;
}

footer {
    margin-top: 50px;
    text-align: center;
    font-size: 0.9em;
    color: #004d40;
}

footer a {
    color: white;
    text-decoration: none;
    transition: color 0.3s ease;
}

footer a:hover {
    color: #004d40;
    text-decoration: underline;
}
</style>
"""

html = """
<h1>GreenShield AI Assistant</h1>
<p>Ask me anything about environmentalism!</p>
"""

html = """
<h1>GreenShield AI Assistant</h1>
<p>Ask me anything about environmentalism!</p>
"""

st.markdown(css, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)

user_input = st.text_input("How can I help you?", key="user_input")

if user_input:
    chat_session = model.start_chat(history=[])
    
    response = chat_session.send_message(user_input)
    
    st.markdown(f"""
    <div id="response-box">
        <p>{response.text}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<footer>
    &copy; 2024 Environmental AI Assistant | Built with 💚 by Atharva.
</footer>
""", unsafe_allow_html=True)
