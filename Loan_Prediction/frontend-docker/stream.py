import streamlit as st
import requests
st.title("Customer Data Input Form")

st.write("""
Please fill in the following details:
- Income: Annual income of the customer.
- CCAvg: Average credit card spending.
- Education: Education level of the customer.
- Mortgage: Mortgage loan balance.
- CD Account: Whether the customer has a CD (Certificate of Deposit) account.
""")

income = st.number_input("Annual Income ($)", min_value=10, max_value=500000, step=1, key="income")
cc_avg = st.number_input("Credit Card Avg. ($)", min_value=0.0, max_value=20.0, step=0.1, key="cc_avg")
education = st.selectbox("Education Level (1=Undergrad, 2=Graduate, 3=Advanced)", [1, 2, 3], key="education")
mortgage = st.number_input("Mortgage ($)", min_value=0, max_value=500000, step=1000, key="mortgage")
cd_account = st.selectbox("CD Account (1=Yes, 0=No)", [1, 0], key="cd_account")

if st.button("Submit"):
    input_data = {
        "Income": income,
        "CCAvg": cc_avg,
        "Education": education,
        "Mortgage": mortgage,
        "CD_Account": cd_account
    }
    st.write("### Input Summary")
    st.write(input_data)

    try:
        response = requests.post("http://backened:8000/predict", json=input_data)
        if response.status_code == 200:
            prediction = response.json().get("prediction", "No prediction returned")
            if prediction.lower() == "approved":
                st.success("Approved")
            else:
                st.error("Rejected")
        else:
            st.error(f"Prediction request failed with status code {response.status_code}")
    except Exception as e:
        st.error(f"Error calling prediction API: {e}")
