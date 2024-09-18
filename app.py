import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import io

# Set page configuration
st.set_page_config(page_title="QR Code Scanner", layout="wide")

# Include FontAwesome for icons
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Logo
st.image("jb.png", width=250)  # Replace with your logo URL

# Navbar
st.markdown("""
<div class="navbar">
  <a href="#Home">Home</a>
  <a href="#About">About</a>
  <a href="#BackToWebsite">Back To Website</a>
</div>
<style>
    .navbar {
        background-color: blue;
        overflow: hidden;
    }
    .navbar a {
        float: left;
        display: block;
        color: #f2f2f2;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    .navbar a:hover {
        background-color: #ddd;
        color: black;
    }
    .footer {
        background-color: blue;
        color: white;
        text-align: center;
        padding: 10px 0;
        position: fixed;
        width: 100%;
        bottom: 0;
    }
    .footer a {
        color: white;
        margin: 0 10px;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    .icon-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Add navigation to different sections
menu = ["Home", "About"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    # Home Page
    st.title("QR Code Scanner")
    st.write("Upload an image containing a QR code and extract its data.")

    # Image upload
    uploaded_file = st.file_uploader("Upload a QR Code image:", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Show the file name
        st.write(f"Uploaded File Name: **{uploaded_file.name}**")

        # Load image using PIL
        image = Image.open(uploaded_file)

        # Decode QR code
        decoded_objects = decode(image)
        if decoded_objects:
            data = decoded_objects[0].data.decode('utf-8')
            st.success(f"QR Code Data: {data}")

            # Download button to download the extracted data
            st.download_button(
                label="📥 Download Text",
                data=data,
                file_name="extracted_text.txt",
                mime="text/plain",
                key="download_button"
            )

            # Copy button using JavaScript
            components.html(f"""
            <script>
            function copyToClipboard() {{
                const text = `{data.replace("`", "\\`")}`;
                navigator.clipboard.writeText(text).then(() => {{
                    alert('Text copied to clipboard!');
                }});
            }}
            </script>
            <button class="icon-btn" onclick="copyToClipboard()">📋 Copy Text</button>
            """, height=50, scrolling=False)
        else:
            st.warning("No data found in the QR code.")

elif choice == "About":
    # About Page
    st.title("About QR Code Scanner")
    st.write("""
    This tool allows you to scan and extract data from QR codes in images.

    **Features**:
    - Upload an image containing a QR code.
    - Extract the data encoded in the QR code.
    - Download or copy the data.

    **Technology Stack**:
    - Streamlit (for building the web app)
    - Pyzbar (for QR code detection and decoding)
    - PIL (for handling images)
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 QR Code Scanner | TechieHelp</p>
    <a href="https://www.linkedin.com/in/techiehelp">LinkedIn</a>
    <a href="https://www.twitter.com/techiehelp">Twitter</a>
    <a href="https://www.instagram.com/techiehelp2">Instagram</a>
</div>
""", unsafe_allow_html=True)
