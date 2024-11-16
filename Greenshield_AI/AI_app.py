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
