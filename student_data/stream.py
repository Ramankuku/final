import streamlit as st
import requests

st.title("Student Placement Prediction")

IQ = st.number_input("IQ", min_value=50, max_value=200, value=100)
CGPA = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.0, step=0.01)
Academic_Performance = st.number_input("Academic Performance", min_value=0, max_value=100, value=75)
Communication_Skills = st.number_input("Communication Skills", min_value=0, max_value=100, value=70)
Projects_Completed = st.number_input("Projects Completed", min_value=0, max_value=50, value=5)

if st.button("Predict"):
    payload = {
        "IQ": IQ,
        "CGPA": CGPA,
        "Academic_Performance": Academic_Performance,
        "Communication_Skills": Communication_Skills,
        "Projects_Completed": Projects_Completed
    }

    # Make the POST request
    response = requests.post("http://0.0.0.0:8000/predict/", json=payload)

    if response.status_code == 200:
        result = response.json()
        prediction = result["prediction"]
        st.success(f"Predicted Result: {prediction}")
    else:
        st.error("API request failed.")
