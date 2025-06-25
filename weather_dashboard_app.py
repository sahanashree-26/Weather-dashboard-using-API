import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Title
st.title("🌤 Weather Forecast Dashboard")
st.write("Enter a city name to view the 5-day weather forecast (in 3-hour steps).")

# Input for city and API key
city = st.text_input("Enter City Name", value="London")
api_key = st.text_input("Enter Your OpenWeatherMap API Key", type="password")

# When the user clicks the button
if st.button("Get Forecast"):
    if not city or not api_key:
        st.error("Please enter both city name and API key.")
    else:
        # Build the API URL
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code != 200:
            st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        else:
            data = response.json()
            forecast_list = data.get('list', [])
            
            # Extract date and temperature
            dates = [item['dt_txt'] for item in forecast_list]
            temps = [item['main']['temp'] for item in forecast_list]

            df = pd.DataFrame({
                'DateTime': pd.to_datetime(dates),
                'Temperature (°C)': temps
            })

            # Plotting
            st.subheader(f"📈 5-Day Temperature Forecast for {city}")
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=df, x='DateTime', y='Temperature (°C)', marker='o')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

            # Show raw data table
            if st.checkbox("Show Raw Data Table"):
                st.dataframe(df)
