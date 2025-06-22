import streamlit as st
import requests


st.title('Generating Blogs')
topic = st.text_input("Enter the blog topic that you want...")

if st.button('Generate Blog'):
    with st.spinner("Generating Blogs..."):
        response = requests.post('http://127.0.0.1:5000/generate', json={"topic": topic})

        if response.status_code == 200:
            result = response.json()
            st.subheader("Blog Generated")
            st.markdown(result['blog'])
        
        else:
            st.error('Error in Generating the blog')
