import os
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
YOUR_API_KEY = os.getenv("AIRVISUAL_API_KEY")

def get_supported_countries():
    url = f"http://api.airvisual.com/v2/countries?key={YOUR_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") == "success":
            countries = data.get("data", [])
            st.subheader("Supported Countries")
            
            if countries:
                for country in countries:
                    st.write(country.get("country"))
            else:
                st.warning("No supported countries found.")
        else:
            st.warning("Failed to fetch supported countries. Please check your API key.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def get_nearest_city_data():
    url = f"http://api.airvisual.com/v2/nearest_city?key={YOUR_API_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()["data"]
        aqi = data["current"]["pollution"]["aqius"]
        humidity = data["current"]["weather"]["hu"]
        temperature = data["current"]["weather"]["tp"]

        st.write(
            f'<div class="responsive-margin" style="display: inline-block; text-align: center;">Detected City: {data["city"]}</div>'
            f'<div class="responsive-margin" style="display: inline-block; text-align: center;">Detected State: {data["state"]}</div>'
            f'<div style="display: inline-block; text-align: center;">Detected Country: {data["country"]}</div>'
            f'<br/>',
            unsafe_allow_html=True
        )

        df = pd.DataFrame({
            "Category": ["AQI", "Humidity (%)", "Temperature (°C)"],
            "Value": [aqi, humidity, temperature]
        })

        df = df.set_index("Category")
        df = df.transpose()
        st.bar_chart(df)

    else:
        st.error("Failed to fetch data. Please check your API key.")



st.set_page_config(page_title="EcoSync", page_icon=":seedling:", layout="wide")

st.header("Welcome to EcoSync!")
st.subheader("Your one-stop platform for getting the latest information about the air quality around you")

with st.container():
    st.write("---")
    get_nearest_city_data()
    st.write("---")

with st.chat_message("user"):
    st.write("Hello :wave:")