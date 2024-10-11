# Import necessary libraries
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import json

# Initialize global variables
__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    """
    Load the saved artifacts (data columns and trained model) from the artifacts folder.
    """
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    # Load the data columns from the JSON file
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    # Load the trained model from the pickle file
    global __model
    if __model is None:
        with open('./artifacts/maryland_home_prices_model.pkl', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    """
    Return the list of location names.
    """
    return __locations

# Load the saved artifacts
load_saved_artifacts()
def get_estimated_price(bed, bath, acre_lot, zip_code, house_size, location):
    """
    Estimate the price of a home based on the given features.
    Args:
        bed (int): Number of bedrooms.
        bath (int): Number of bathrooms.
        acre_lot (float): Lot size in acres.
        zip_code (int): Zip code.
        house_size (int): Size of the house in square feet.
        location (str): Location of the house.

    Returns:
        float: Estimated price of the home.
    """
    try:
        # Get the index of the location in the data columns
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    # Create a feature vector with zeros
    x = np.zeros(len(__data_columns))
    x[0] = bed
    x[1] = bath
    x[2] = acre_lot
    x[3] = zip_code
    x[4] = house_size
    if loc_index >= 0:
        x[loc_index] = 1

    # Make the prediction using the trained model
    return round(__model.predict([x])[0], 2)

# Create the Streamlit app
st.title("Maryland Home Price Predictor")

# Create input fields for the user
st.subheader("Enter Home Details")

col1, col2 = st.columns(2)
with col1:
    bedrooms = st.selectbox("Number of Bedrooms", range(1, 11))
    bathrooms = st.selectbox("Number of Bathrooms", range(1, 11))
    lot_size = st.number_input("Lot Size (acres)", min_value=0.01, max_value=100.0, value=0.59)

with col2:
    zip_code = st.text_input("Zip Code", value="21001")
    sqft = st.number_input("Square Feet", min_value=500, max_value=10000, value=1832)
    city = st.text_input("City", value="Aberdeen")

# Create a submit button
if st.button("Submit"):
    # Make prediction and display result
    predicted_price = get_estimated_price(bedrooms, bathrooms, lot_size, zip_code, sqft, city)
    st.subheader("Predicted Price:")
    # Write formatted predicted price
    st.success(f"${predicted_price:,.2f}")
