import streamlit as st 
from PIL import Image
import numpy as np
import base64
from io import BytesIO

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format='TIFF')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/tiff;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Get the cover image from the user
def encryptPage():
    cover_file = st.file_uploader('Enter RGB image file', type=['png', 'jpg', 'bmp'])
    if cover_file is not None:
        cover = Image.open(cover_file)

        # Get the message image from the user
        message_file = st.file_uploader('Enter CMYK image file', type=['png', 'jpg', 'bmp'])
        if message_file is not None:
            message = Image.open(message_file)

            # Convert the CMYK image to RGB
            message = message.convert("RGB")

            # Change to double to work with addition below
            cover = np.array(cover, dtype=np.uint8)
            message = np.array(message, dtype=np.uint8)

            # Imbed = no. of bits of message image to embed in cover image
            imbed = 4

            # Shift the message image over (8-imbed) bits to right
            messageshift = message >> (8-imbed)

            # Show the message image with only embed bits on screen
            # Must shift from LSBs to MSBs
            showmess = messageshift << (8-imbed)

            # Now zero out imbed bits in cover image
            coverzero = cover & (255 << imbed)

            # Now add message image and cover image
            stego = coverzero + messageshift

            # Display the stego image
            st.image(stego, caption='Stego image')

            # Now add message image and cover image
            stego = coverzero + messageshift

            # Convert the stego array back to an image
            stego_img = Image.fromarray(stego.astype(np.uint8))

            # Add a download link for the stego image
            st.markdown(get_image_download_link(stego_img, 'stego.tiff', 'Download stego image'), unsafe_allow_html=True)