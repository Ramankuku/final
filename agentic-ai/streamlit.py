# frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="LangChain Multi-Agent", layout="wide")
st.title("🧠 AI Multi-Agent Assistant")

st.markdown("""
This assistant can:
- 🔍 Search the Web
- 🌤 Get Weather
- 📄 Upload PDF & Ask Questions
- ➗ Solve Math Expressions
""")

# Upload PDF
uploaded_pdf = st.file_uploader("📄 Upload a PDF", type="pdf")

if uploaded_pdf:
    with st.spinner("Uploading and indexing PDF..."):
        try:
            files = {"pdf_file": uploaded_pdf}
            res = requests.post("http://127.0.0.1:8000/upload_pdf", files=files)
            if res.status_code == 200:
                st.success("✅ PDF uploaded and processed!")
            else:
                st.error("❌ Failed to upload PDF.")
        except Exception as e:
            st.error(f"❌ Upload Error: {str(e)}")

# Ask a question
question = st.text_input("💬 Ask a question about the PDF or anything...")

if st.button("Submit") and question:
    with st.spinner("🤖 Thinking..."):
        try:
            res = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
            response = res.json()
            st.success(response.get("answer", "No answer returned."))
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
