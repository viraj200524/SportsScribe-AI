import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdown2
from xhtml2pdf import pisa
import tempfile
import base64
import os

st.set_page_config(layout="wide")
st.title("Markdown Report Viewer")

# Store markdown content across interactions
if 'markdown_content' not in st.session_state:
    st.session_state.markdown_content = ""

# Create a row with 2 columns to simulate "top right"
col_left, col_right = st.columns([7, 1])

with col_right:
    if st.session_state.markdown_content:
        if st.button("💾 Save Report"):
            # Convert markdown to HTML
            html = markdown2.markdown(st.session_state.markdown_content)

            # Generate PDF using xhtml2pdf
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdf_path = tmp_pdf.name

            # Write HTML to PDF file
            with open(pdf_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html, dest=pdf_file)

            if not pisa_status.err:
                with open(pdf_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">📄 Click here to download your report</a>'
                st.markdown(href, unsafe_allow_html=True)
                # Optional: cleanup can be done later automatically
                # os.remove(pdf_path)
            else:
                st.error("Failed to generate PDF.")

# Input area
input_text = st.text_area("Enter your text", height=200)

# Generate Report button
if st.button("Generate Report"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/get_report",
                json={"input": input_text}
            )
            response.raise_for_status()

            # Extract markdown from response HTML
            soup = BeautifulSoup(response.text, "html.parser")
            markdown_div = soup.find(class_="language-markdown")

            if markdown_div:
                markdown_text = markdown_div.get_text()
                st.session_state.markdown_content = markdown_text
                st.markdown(markdown_text, unsafe_allow_html=True)
            else:
                st.error("Could not find markdown content in the response.")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
