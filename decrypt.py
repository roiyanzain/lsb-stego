import streamlit as st
from PIL import Image
import numpy as np
import base64
from io import BytesIO

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format='TIFF')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/TIFF;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Get the stego image from the user
def decryptPage():
    stego_file = st.file_uploader('Enter stego image file', type=['png', 'jpg', 'bmp', 'tiff'])
    if stego_file is not None:
        stego = Image.open(stego_file)

        # Change to double for manipulation
        stego = np.array(stego, dtype=np.uint8)

        # Initialize the extracted message
        extracted_message = np.zeros(stego.shape, dtype=np.uint8)

        # Imbed = no. of bits of message image to embed in cover image
        imbed = 4

        # Extract the least significant bits from the stego image
        for i in range(imbed):
            extracted_message = extracted_message | ((stego & (1 << i)) << (8 - imbed))

        # Convert the extracted message back to CMYK
        extracted_message = Image.fromarray(extracted_message)
        extracted_message = extracted_message.convert("CMYK")

        # Display the extracted message
        st.image(extracted_message, caption='Extracted Message')

        # Add a download link for the stego image
        st.markdown(get_image_download_link(extracted_message, 'result.jpg', 'Download extracted image'), unsafe_allow_html=True)