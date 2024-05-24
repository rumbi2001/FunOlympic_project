import streamlit as st
import pandas as pd
import csv
from random import randint, choice
from faker import Faker
from dashboard import display_dashboard  # Import the dashboard function
from reports_page import display_reports  # Import the reports page function
from prediction_page import display_prediction_page  # Import the reports page function

# Load CSS
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    # Your data loading logic here
    pass

# Define functions for generating logs, saving logs to CSV, etc.
# ...

# Define pages
def home_page():
    st.title('Welcome to the FunOlympics Home Page')
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    
    # Display images with a space between them
    col1, empty_col, col2 = st.columns([1.8, 0.2, 2])
    with col1:
        st.image("images/Olympics.jpg", width=350)
    with col2:
        st.image("images/countries.jpg", width=330)
    
    # Add content for the home page
    st.write("""
    <div style="text-align: justify">
   Arecham Solutions Inc. is a leading IT services company specialising in providing innovative solutions to 
   businesses across various industries. Established in 2010 by a group of seasoned technology professionals, 
   the company has rapidly grown into a trusted partner for organizations seeking to leverage cutting-edge 
   technologies to drive growth and success. The mission of the company is to empower businesses with intelligent 
   technology solutions that unlock their full potential and drive sustainable growth. Arecham specializes in providing
   comprehensive IT services with a strong emphasis on business intelligence and data analytics. Through advanced data
   analytics and visualisation techniques, it helps clients derive actionable insights from their data, enabling informed 
   decision-making and strategic planning.
             
   Recently, Arecham Solutions Inc. secured a contract with FunOlympic to develop tools that will allow the client to 
   analyse the success of the broadcast platform. Arecham has successfully completed two notable projects: crafting a 
   tailored business intelligence platform for a travel firm, using web server logs to analyse visitor data, and 
   implementing predictive analytics for a healthcare provider to optimize patient care. These projects highlight the 
   company’s ability to extract valuable insights from web server logs, contributing to data-driven decision-making and
   client success.

    </div>
    """, unsafe_allow_html=True)

    # Display images with a space between them
    col1, empty_col, col2 = st.columns([1.8, 0.2, 2])
    with col1:
        st.image("images/basketball.jpg", width=350)
    with col2:
        st.image("images/swimming.jpg", width=320)

def dashboard():
    display_dashboard()  # Call the function to display the dashboard

def reports_page():
    display_reports()  # Call the function to display the reports

def prediction_page():
    display_prediction_page() # Call the function to display the predictions

# Define navigation
pages = {
    "Home": home_page,
    "Dashboard": dashboard,
    "Standalone Reports": reports_page,
    "Machine Learning Prediction": prediction_page,
}

# Sidebar navigation
st.sidebar.title('Navigation')

# Add the image to the sidebar
st.sidebar.image("images/touch.webp", width=250)

selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page
pages[selection]()
