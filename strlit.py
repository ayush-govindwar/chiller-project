import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Create a title for the app
st.title("Chill Load Predictor")

# Add a navigation menu
pages = ["Home", "About", "Services", "Contact"]
page = st.sidebar.selectbox("Navigation", pages)

if page == "Home":
    # Create a file uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Create a button to trigger the prediction
    if st.button("Predict Chill Load"):
        if uploaded_file is not None:
            # Send the file to the FastAPI endpoint
            response = requests.post("http://localhost:3000/predict", files={"csv_file": uploaded_file})

            # Check if the response was successful
            if response.status_code == 200:
                # Get the updated CSV data from the response
                updated_csv = response.content

                # Create a BytesIO object to hold the updated CSV data
                updated_csv_bytes = BytesIO(updated_csv)

                # Create a button to download the updated CSV file
                st.download_button("Download Updated CSV", updated_csv_bytes, file_name="updated_" + uploaded_file.name)

            else:
                st.error("Failed to predict chiller load")
        else:
            st.error("Please upload a CSV file")

elif page == "About":
    st.header("About Us")
    st.write("Welcome to Chill Load Predictor! We are a team of experts in machine learning and data science, dedicated to providing accurate and reliable chill load predictions for your business.")

elif page == "Services":
    st.header("Our Services")
    st.write("We offer a range of services to help you optimize your chill load predictions, including:")
    st.markdown("- Data analysis and visualization")
    st.markdown("- Machine learning model development")
    st.markdown("- Customized chill load prediction solutions")

elif page == "Contact":
    st.header("Get in Touch")
    st.write("Have a question or want to learn more about our services? Contact us at:")
    st.write("Email: [info@chillloadpredictor.com](mailto:info@chillloadpredictor.com)")
    st.write("Phone: 555-555-5555")
    st.write("Address: 123 Main St, Anytown, USA")

# Add CSS styling
st.markdown("""<style>
            h1 {
                color: green;
                font-size: 36px;
                text-align: center;
                padding: 20px;
            }

            .stFileUploader {
                margin-top: 20px;
                margin-bottom: 20px;
            }

            .stButton {
                background-color: #4CAF50;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            .stButton:hover {
                background-color: #3e8e41;
            }

            .stError {
                color: #f44336;
                font-size: 16px;
                margin-top: 10px;
            }
</style>""", unsafe_allow_html=True)