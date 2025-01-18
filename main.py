import streamlit as st
import numpy as np
import pandas as pd
import datetime
import xgboost as xgb

# Load the model
model = xgb.XGBRegressor()
model.load_model('xgb_model.json')

# Current date and time
date_time = datetime.datetime.now()

# Main function
def main(): 
    # Page title and branding
    st.set_page_config(page_title="AutoCents", page_icon="🚗", layout="wide")

    # Header with a centered title
    st.markdown(
        """
        <div style="text-align: center; background-color: #f0f8ff; padding: 16px;">
            <h1 style="color: #333;">AutoCents 🚗</h1>
            <p style="color: #666; font-size: 18px;">Your Reliable Car Price Prediction Companion</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Sidebar
    st.sidebar.header("About AutoCents")
    st.sidebar.write(
        """
        AutoCents leverages Machine Learning to predict the resale value of your car based on key parameters.
        
        **How it works:**
        - Input car details.
        - Predict the estimated resale price.
        
        Developed using XGBoost and Streamlit.
        """
    )
    st.sidebar.image("https://via.placeholder.com/250", caption="AutoCents Logo", use_column_width=True)

    # Main content
    st.markdown("## Are you planning to sell your car? 🚘\n### Let's evaluate its resale price!")
    st.write("Provide the details below, and we'll predict the resale price.")

    # User inputs with columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        p1 = st.number_input(
            'Current ex-showroom price of the car (in Lakhs):', 2.5, 25.0, step=1.0, format="%.1f"
        )
        p2 = st.number_input(
            'Distance completed by the car (in Kilometers):', 100, 50000000, step=100
        )
        s1 = st.selectbox('Fuel type of the car:', ('Petrol', 'Diesel', 'CNG'))
        p3 = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}[s1]

    with col2:
        s2 = st.selectbox('Are you a dealer or an individual?', ('Dealer', 'Individual'))
        p4 = {'Dealer': 0, 'Individual': 1}[s2]
        s3 = st.selectbox('Transmission type:', ('Manual', 'Automatic'))
        p5 = {'Manual': 0, 'Automatic': 1}[s3]
        p6 = st.slider("Number of previous owners:", 0, 3, step=1)
        years = st.number_input('Year the car was purchased:', 1990, date_time.year, step=1)
        p7 = date_time.year - years

    # Data preparation for prediction
    data_new = pd.DataFrame({
        'Present_Price': p1,
        'Kms_Driven': p2,
        'Fuel_Type': p3,
        'Seller_Type': p4,
        'Transmission': p5,
        'Owner': p6,
        'Age': p7
    }, index=[0])

    # Prediction button
    if st.button('Predict Resale Value'):
        try:
            prediction = model.predict(data_new)
            if prediction > 0:
                st.balloons()
                st.success(f'You can sell the car for **₹{prediction[0]:,.2f} Lakhs**!')
            else:
                st.warning("Unfortunately, this car might not be sellable at a reasonable price.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Footer
    st.markdown(
        """
        <hr>
        <footer style="text-align: center; color: #888;">
            <p>© 2024 AutoCents. All Rights Reserved.</p>
        </footer>
        """, unsafe_allow_html=True
    )

# Run the app
if __name__ == '__main__':
    main()
