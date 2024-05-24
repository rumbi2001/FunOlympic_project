import streamlit as st
import pandas as pd
import altair as alt

# Load data with caching
@st.cache_data
def load_report_data():
    try:
        # Load the CSV file
        data = pd.read_csv('web_server_logs.csv', names=[
            'Timestamp', 'IP Address', 'Method', 'Endpoint', 'Status', 
            'Country', 'Sports Activity', 'Device', 'Browser', 'Duration'
        ])
        return data
    except FileNotFoundError:
        st.error("Error: Report data CSV file not found.")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def display_reports():
    st.title('Standalone Reports Page Analysis')
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    # Load data
    report_data = load_report_data()
    if report_data.empty:
        st.write("No data available.")
        return

    # Interactive selection for linking visualizations
    selection = alt.selection_multi(fields=['Endpoint'], name='endpoint_selection')

    # 1) Table showcasing country, device, browser, endpoint
    st.subheader('Logs Table')
    st.write(report_data[['Country', 'Device', 'Browser', 'Endpoint']])

    # 2) Horizontal bar plot to show total number of visits by endpoint
    st.subheader('Total Number of Visits by Endpoint')
    visits_by_endpoint = report_data['Endpoint'].value_counts().reset_index()
    visits_by_endpoint.columns = ['Endpoint', 'Count']
    bar_chart = alt.Chart(visits_by_endpoint).mark_bar().encode(
        x='Count:Q',
        y=alt.Y('Endpoint:N', sort='-x'),
        color=alt.Color('Endpoint:N', scale=alt.Scale(scheme='category20')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=['Endpoint:N', 'Count:Q']
    ).add_selection(
        selection
    ).properties(
        title=''
    )

    st.altair_chart(bar_chart, use_container_width=True)

    # 3) Total number of people clicking on different sports to watch
    st.subheader('Clicks on Different Sports')
    clicks_by_sports = report_data['Sports Activity'].value_counts().reset_index()
    clicks_by_sports.columns = ['Sports Activity', 'Count']
    pie_chart = alt.Chart(clicks_by_sports).mark_arc().encode(
        theta='Count:Q',
        color=alt.Color('Sports Activity:N', scale=alt.Scale(scheme='category20')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=['Sports Activity:N', 'Count:Q']
    ).properties(
        title=''
    ).add_selection(
        selection
    )

    st.altair_chart(pie_chart, use_container_width=True)

# This should be called in `app.py`, so no need to run it here
