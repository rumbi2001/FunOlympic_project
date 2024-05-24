import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

@st.cache_data
def load_data():
    """
    Load the web server log data for prediction.

    Returns:
        pd.DataFrame: A DataFrame containing the web server log data.
    """
    try:
        # Load the CSV file
        data = pd.read_csv('web_server_logs.csv', names=[
            'Timestamp', 'IP Address', 'Method', 'Endpoint', 'Status', 
            'Country', 'Sports Activity', 'Device', 'Browser', 'Duration'
        ], skiprows=1)  # Skip the header row

        # Convert Timestamp to datetime
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y-%m-%d %H:%M:%S')

        return data
    except FileNotFoundError:
        st.error("Error: Web server log CSV file not found.")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def train_model(data):
    """
    Train a simple linear regression model using only positive durations.

    Args:
        data (pd.DataFrame): DataFrame containing the training data.

    Returns:
        sklearn.linear_model.LinearRegression: Trained linear regression model.
    """
    # Filter out non-positive durations
    data = data[data['Duration'] > 0]

    # Extract hour from Timestamp
    data['Hour'] = data['Timestamp'].dt.hour

    X = data[['Hour']]  # Features
    y = data['Duration']  # Target variable

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    st.write(f"Mean Squared Error: {mse}")

    return model

def predict_peak_visiting_time(model, hour):
    """
    Predict the peak visiting time by visitors.

    Args:
        model (sklearn.linear_model.LinearRegression): Trained linear regression model.
        hour (int): Hour of the day for prediction.

    Returns:
        float: Predicted duration of visits.
    """
    prediction = model.predict([[hour]])
    return prediction[0]

def display_prediction_page():
    """
    Display the prediction page.
    """
    st.title('Peak Duration Visit Time Predictor')

    # Load data
    data = load_data()

    if data.empty:
        st.write("No data available for prediction.")
        return

    # Train model
    model = train_model(data)

    # Prediction input
    hour = st.slider('Select hour:', 0, 23, 12)  # Default value is 12

    # Predict peak visiting time
    prediction = predict_peak_visiting_time(model, hour)

    st.write(f"Predicted duration of visits at {hour}:00: {int(prediction)} seconds")

if __name__ == '__main__':
    display_prediction_page()
