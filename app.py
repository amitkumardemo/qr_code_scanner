import streamlit as st
import numpy as np
from PIL import Image
import cv2

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
        try:
            # Load image using PIL
            image = Image.open(uploaded_file)

            # Display image info for debugging
            st.write("Image format:", image.format)
            st.write("Image mode:", image.mode)
            st.write("Image size:", image.size)

            # Convert the image to RGB if not already in RGB format
            if image.mode == '1':  # Binary image mode
                image = image.convert('L')  # Convert to grayscale
            elif image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert the image to a numpy array
            image_np = np.array(image)

            # Convert the image from RGB (PIL) to BGR (OpenCV)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

            # Display converted image info for debugging
            st.write("Converted image shape:", image_np.shape)

            # QR code detection using OpenCV
            qr_detector = cv2.QRCodeDetector()
            retval, decoded_info, points, _ = qr_detector.detectAndDecode(image_np)

            if retval:
                data = decoded_info
                st.success(f"QR Code Data: {data}")

                # Show the uploaded image
                st.image(image, caption="Uploaded QR Code Image", use_column_width=True)

                # Download button
                st.download_button(
                    label="📥 Download Text",
                    data=data,
                    file_name="extracted_text.txt",
                    mime="text/plain",
                    key="download_button"
                )

                # Copy button using JavaScript
                st.components.v1.html(f"""
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
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif choice == "About":
    # About Page
    st.title("About QR Code Scanner")
    st.write("""
    This tool allows you to scan and extract data from QR codes in images.

    **Features**:
    - Upload an image containing a QR code.
    - Extract the data encoded in the QR code.

    **Technology Stack**:
    - Streamlit (for building the web app)
    - OpenCV (for QR code detection and decoding)
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
