import streamlit as st
import requests
import json

# Title and description of the app
st.title("Smart Retail System Management with Generative AI")
st.write("Manage products, check stock levels, and get AI-based assistance on retail products.")

# API key input from the user
api_key = st.text_input("Enter your API Key", type="password")

# Simulate the backend API base URL (you will replace this with the actual API URL)
BASE_API_URL = "https://api.smartretail.com"

# Check if API key is provided
if api_key:
    st.success("API Key provided successfully!")
    
    # Function to fetch product stock details
    def fetch_product_stock(product_id):
        url = f"{BASE_API_URL}/product/{product_id}/stock"
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error fetching product stock. Please check the API key and product ID.")
            return None

    # Function to get AI-based product guidance
    def get_ai_assistance(product_query):
        ai_url = f"{BASE_API_URL}/ai/assist"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {"query": product_query}
        response = requests.post(ai_url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            st.error("Error with AI assistance. Please check the API key or your query.")
            return None

    # Selectbox for user to choose action
    action = st.selectbox("Choose Action", ["Check Product Stock", "Get AI Product Guidance"])

    if action == "Check Product Stock":
        product_id = st.text_input("Enter Product ID")
        if st.button("Fetch Stock Details"):
            if product_id:
                product_info = fetch_product_stock(product_id)
                if product_info:
                    st.write(f"Product ID: {product_info['product_id']}")
                    st.write(f"Product Name: {product_info['product_name']}")
                    st.write(f"Stock Left: {product_info['stock_left']}")
                    st.write(f"Price: {product_info['price']}")
            else:
                st.error("Please enter a valid Product ID.")

    elif action == "Get AI Product Guidance":
        product_query = st.text_input("Enter your question about a product (e.g., 'What is the best laptop for gaming?')")
        if st.button("Get AI Assistance"):
            if product_query:
                ai_response = get_ai_assistance(product_query)
                if ai_response:
                    st.write(f"AI Response: {ai_response}")
            else:
                st.error("Please enter a valid query.")

else:
    st.warning("Please enter an API key to proceed.")
