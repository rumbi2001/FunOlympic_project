import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
from random import randint, choice
from faker import Faker
import altair as alt


fake = Faker()

# Function to generate random IP address
def generate_ip():
    return ".".join(map(str, (randint(0, 255) for _ in range(4))))

# Function to generate log entries
def generate_logs(num_entries=200):
    endpoints = ["/index.html", "/images/games.jpg", "/searchsports.php", "/football.html"]
    methods = ["GET", "POST"]
    statuses = [200, 304, 404, 500]
    countries = [fake.country() for _ in range(100)]
    devices = ["Desktop", "Mobile", "Tablet"]
    browsers = ["Chrome", "Firefox", "Safari", "Edge"]
    sports_activities = ["Football", "Basketball", "Tennis", "Swimming", "Running", "Cycling", "Golf", "Baseball", "Cricket", "Volleyball"]

    log_entries = []
    start_time = datetime.now()

    for _ in range(num_entries):
        timestamp = (start_time + timedelta(seconds=randint(0, 100000))).strftime('%Y-%m-%d %H:%M:%S')
        ip_address = generate_ip()
        method = choice(methods)
        endpoint = choice(endpoints)
        status = choice(statuses)
        country = choice(countries)
        sports_activity = choice(sports_activities)
        device = choice(devices)
        browser = choice(browsers)
        duration = randint(1, 1000)  # Random duration between 1 and 1000 seconds
        log_entries.append([timestamp, ip_address, method, endpoint, status, country, sports_activity, device, browser, duration])

    return log_entries

# Function to save log entries to a CSV file
def save_logs_to_csv(log_entries, filename="web_server_logs.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:  # Use 'a' to append data
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Timestamp", "IP Address", "Method", "Endpoint", "Status", "Country", "Sports Activity", "Device", "Browser", "Duration"])
        writer.writerows(log_entries)

# Function to convert DataFrame to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Load data with caching
@st.cache_data
def load_data():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        data = pd.read_csv('web_server_logs.csv')
        return data, timestamp
    except FileNotFoundError:
        st.error("Error: CSV file not found.")
    except KeyError:
        st.error("Error: Missing columns in CSV file.")
        return pd.DataFrame(), timestamp  # Return an empty DataFrame in case of error

def display_dashboard():
    logs, timestamp = load_data()

    if not logs.empty:
        st.title('Web Server Log Analysis Dashboard')
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

        # Display timestamp
        st.write(f"Data fetched at: {timestamp}")

        # Buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button("Generate Logs"):
            log_entries = generate_logs()
            save_logs_to_csv(log_entries)
            st.success("Log files generated successfully.")
        if col2.button("View Logs"):
            st.dataframe(logs)
        if col3.button("Trim Logs"):
            logs = logs.head(10)
            st.write("Logs trimmed to the first 10 entries.")
            st.dataframe(logs)
        if col4.button("Convert to CSV"):
            csv_data = convert_df_to_csv(logs)
            st.download_button(
                label="Download data as CSV",
                data=csv_data,
                file_name='trimmed_logs.csv',
                mime='text/csv',
            )
        if col5.button("Download Logs"):
            csv_data = convert_df_to_csv(logs)
            st.download_button(
                label="Download original data as CSV",
                data=csv_data,
                file_name='web_server_logs.csv',
                mime='text/csv',
            )

        # Filtering options
        st.sidebar.header('Filters')
        countries = st.sidebar.multiselect('Select Countries', logs['Country'].unique())
        sports_activities = st.sidebar.multiselect('Select Sports Activities', logs['Sports Activity'].unique())
        endpoints = st.sidebar.multiselect('Select Endpoints', logs['Endpoint'].unique())
        devices = st.sidebar.multiselect('Select Devices', logs['Device'].unique())
        browsers = st.sidebar.multiselect('Select Browsers', logs['Browser'].unique())

        filtered_logs = logs
        if countries:
            filtered_logs = filtered_logs[filtered_logs['Country'].isin(countries)]
        if sports_activities:
            filtered_logs = filtered_logs[filtered_logs['Sports Activity'].isin(sports_activities)]
        if endpoints:
            filtered_logs = filtered_logs[filtered_logs['Endpoint'].isin(endpoints)]
        if devices:
            filtered_logs = filtered_logs[filtered_logs['Device'].isin(devices)]
        if browsers:
            filtered_logs = filtered_logs[filtered_logs['Browser'].isin(browsers)]

        # Display visualizations side by side
        st.header('')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Number of Visits per Country')
            visits_per_country = filtered_logs['Country'].value_counts().reset_index()
            visits_per_country.columns = ['Country', 'count']
            chart = alt.Chart(visits_per_country).mark_bar().encode(
                x='Country',
                y='count',
                color=alt.Color('Country', scale=alt.Scale(scheme='category20')),
                tooltip=['Country', 'count']  # Add tooltip for interactivity
            ).interactive()  # Make the chart interactive
            st.altair_chart(chart, use_container_width=True)

        with col2:
            st.subheader('Main Interests based on Viewed Endpoints')
            main_interests = filtered_logs['Endpoint'].value_counts().reset_index()
            main_interests.columns = ['Endpoint', 'count']
            chart = alt.Chart(main_interests).mark_bar().encode(
                x='Endpoint',
                y='count',
                color=alt.Color('Endpoint', scale=alt.Scale(scheme='category20')),
                tooltip=['Endpoint', 'count']  # Add tooltip for interactivity
            ).interactive()  # Make the chart interactive
            st.altair_chart(chart, use_container_width=True)       

        # Total Visits by Device and Average Response Time by Browser
        st.header('')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Total Visits by Device')
            visits_by_device = filtered_logs['Device'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(visits_by_device, labels=visits_by_device.index, autopct='%1.1f%%', startangle=90)
            ax1.legend(visits_by_device.index, loc="best", fontsize='small')
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

        with col2:
            st.subheader('Average Response Time by Browser')
            avg_response_time_by_browser = filtered_logs.groupby('Browser')['Duration'].mean().reset_index()
            avg_response_time_by_browser.columns = ['Browser', 'Average Response Time']
            chart = alt.Chart(avg_response_time_by_browser).mark_bar().encode(
                y=alt.Y('Browser:N', sort='-x'),
                x=alt.X('Average Response Time:Q'),
                color=alt.Color('Browser:N', scale=alt.Scale(scheme='category20'))  # Different colors for each browser
            )
            st.altair_chart(chart, use_container_width=True)

        # Visitors Access Analysis
        st.header('Visitors Access Analysis')

        if 'Endpoint' in filtered_logs.columns:
            endpoint = st.selectbox('Select Endpoint', filtered_logs['Endpoint'].unique())
            
            if endpoint:
                endpoint_data = filtered_logs[filtered_logs['Endpoint'] == endpoint]

                data = {
                    'Metric': ['Average Visits', 'Standard Deviation'],
                    'Value': [endpoint_data.shape[0], endpoint_data.shape[0] ** 0.5]  # Using sample size for std dev approximation
                }
                st.table(data)
            else:
                st.write("Please select an endpoint.")
        else:
            st.write("Endpoint column not found.")

# Running the Streamlit app
if __name__ == "__main__":
    display_dashboard()
