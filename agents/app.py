import streamlit as st
import requests
from bs4 import BeautifulSoup
from ReportSavingAgent import get_file_path

st.set_page_config(layout="wide")
st.title("Markdown Report Viewer")

# --- Sidebar Download Button (Always Visible) ---
with st.sidebar:
    st.markdown("### 📥 Download Section")
    
    if st.button("⬇️ Prepare DOCX Report for Download"):
        # Save state to indicate user clicked download button
        st.session_state.download_requested = True

    # If download is requested, handle logic
    if st.session_state.get("download_requested", False):
        docx_file_path = get_file_path()
        if docx_file_path:
            try:
                download_url = f"http://127.0.0.1:8000/download-docx?filepath={docx_file_path}"
                response = requests.get(download_url)
                response.raise_for_status()

                # Streamlit download button (with actual download data)
                st.download_button(
                    label="✅ Click to Download DOCX",
                    data=response.content,
                    file_name=docx_file_path.split("/")[-1],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

                # Reset trigger after download button is rendered
                st.session_state.download_requested = False

            except requests.RequestException as e:
                st.error(f"Download failed: {e}")
        else:
            st.warning("No file path returned. Please generate a report first.")

# --- Main UI for Input and Markdown Display ---
input_text = st.text_area("Enter your text", height=100)

if st.button("Generate Report"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/get_report",
                json={"input": input_text + " Save the report."}
            )
            response.raise_for_status()

            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            markdown_div = soup.find(class_="language-markdown")

            if markdown_div:
                st.markdown(markdown_div.get_text(), unsafe_allow_html=True)
            else:
                st.error("Could not find markdown content in the response.")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
