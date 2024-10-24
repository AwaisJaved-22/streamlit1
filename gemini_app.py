import streamlit as st
import requests
import hmac
import hashlib
import base64
import time
import json

# Set Gemini API key and secret
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'.encode()

# Function to create the request headers
def create_gemini_headers(payload):
    encoded_payload = base64.b64encode(json.dumps(payload).encode())
    signature = hmac.new(API_SECRET, encoded_payload, hashlib.sha384).hexdigest()
    return {
        'Content-Type': 'text/plain',
        'X-GEMINI-APIKEY': API_KEY,
        'X-GEMINI-PAYLOAD': encoded_payload,
        'X-GEMINI-SIGNATURE': signature,
    }

# Streamlit app
st.title("Gemini API Interface")

# Create user options for actions (market data, balances)
option = st.selectbox("Select Action", ["View Market Data", "Check Account Balance"])

# Handle option selection
if option == "View Market Data":
    st.subheader("Market Data")

    # Input for market ticker
    ticker = st.text_input("Enter the ticker (e.g., btcusd):", "btcusd")

    # Call Gemini public API for ticker data
    response = requests.get(f'https://api.gemini.com/v1/pubticker/{ticker}')
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        st.write(f"Last Price: {data['last']}")
        st.write(f"Bid: {data['bid']}")
        st.write(f"Ask: {data['ask']}")
        st.write(f"24hr Volume: {data['volume']}")
    else:
        st.error("Error fetching market data. Please check the ticker.")

elif option == "Check Account Balance":
    st.subheader("Account Balance")

    # Get timestamp and create the payload for private API call
    endpoint = "/v1/balances"
    payload = {
        'request': endpoint,
        'nonce': int(time.time() * 1000)
    }

    # Send POST request with headers
    headers = create_gemini_headers(payload)
    response = requests.post(f'https://api.gemini.com{endpoint}', headers=headers)
    
    # Check if response is successful
    if response.status_code == 200:
        balances = response.json()
        st.write("Balances:")
        for balance in balances:
            st.write(f"Currency: {balance['currency']}, Amount: {balance['amount']}")
    else:
        st.error("Error fetching balance. Please check API keys and permissions.")
