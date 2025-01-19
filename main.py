import streamlit as st
import numpy as np
import pandas as pd
import datetime
import joblib

# Load the model using joblib
try:
    model = joblib.load('car_price.pkl')  # Ensure the path is correct
except Exception as e:
    st.warning("Failed to load model: " + str(e))

# Function to run the Streamlit app
def main():
    html_temp = """
     <div style="background-color:lightblue;padding:16px">
     <h2 style="color:black;text-align:center;">AutoCents</h2>
     <br> 
     </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.write('')
    st.markdown("##### Planning to sell your car? Let's estimate its price!")
    st.write('')
    st.write('')

    # Inputs
    p1 = st.number_input('Current ex-showroom price of the car (In Lakhs)', 2.5, 25.0, step=1.0)
    p2 = st.number_input('Distance completed by the car in Kilometers', 100, 50000000, step=100)
    s1 = st.selectbox('Fuel Type', ('Petrol', 'Diesel', 'CNG'))
    p3 = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}[s1]
    s2 = st.selectbox('Seller Type', ('Dealer', 'Individual'))
    p4 = {'Dealer': 0, 'Individual': 1}[s2]
    s3 = st.selectbox('Transmission Type', ('Manual', 'Automatic'))
    p5 = {'Manual': 0, 'Automatic': 1}[s3]
    p6 = st.slider("Number of Previous Owners", 0, 3)
    years = st.number_input('Year of Purchase', 1990, datetime.datetime.now().year, step=1)
    p7 = datetime.datetime.now().year - years

    data_new = pd.DataFrame({
        'Present_Price': p1,
        'Kms_Driven': p2,
        'Fuel_Type': p3,
        'Seller_Type': p4,
        'Transmission': p5,
        'Owner': p6,
        'Age': p7
    }, index=[0])

    # Prediction
    try:
        if st.button('Predict'):
            prediction = model.predict(data_new)
            if prediction > 0:
                st.balloons()
                st.success(f'Estimated Selling Price: ₹{prediction[0]:.2f} Lakhs')
            else:
                st.warning("The car may not fetch a significant price.")
    except Exception as e:
        st.warning("Prediction failed: " + str(e))

if __name__ == '__main__':
    main()
