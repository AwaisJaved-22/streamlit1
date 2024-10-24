import streamlit as st
import requests

# Placeholder for Gemini API Key
API_KEY = "AIzaSyBLuUyjbUhw_C_nrQx5DI1u-hZBst7JEF4"

# URL for the Gemini API endpoint (replace with actual Gemini API endpoint)
GEMINI_API_URL = "https://api.gemini.com/v1/chat"

# Function to query the chatbot via Gemini API
def get_gemini_response(prompt):
    try:
        # Check if the API key is a placeholder
        if API_KEY == "t":
            return "Please replace the placeholder API key with your actual Gemini API key."

        # Prepare headers and payload for the API request
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "prompt": prompt,
            "max_tokens": 100
        }

        # Make the request to Gemini API (assuming it's a POST request)
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        
        # Parse the response and handle errors
        if response.status_code == 200:
            return response.json().get('response', "No response from the Gemini API.")
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app layout
st.title("Gem