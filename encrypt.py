import streamlit as st 
from PIL import Image
import numpy as np
import base64
from io import BytesIO

# Fungsi untuk mendownload gambar stego ke dalam bentuk 'PNG'
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format='png')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Fungsi untuk menyesuaikan ukuran cover dengan ukuran message
def resize_image(cover, message):
    return cover.resize(message.size)

# Fungsi enkripsi gambar
def encryptPage():
    st.markdown("<h4 style='text-align: left;'>Upload Cover Image</h4>", unsafe_allow_html=True)
    cover_file = st.file_uploader('', type=['png', 'jpg', 'bmp'], key="cover")
    if cover_file is not None:
        cover = Image.open(cover_file)

        # Get the message image from the user
        st.markdown("<h4 style='text-align: left;'>Upload Message Image</h4>", unsafe_allow_html=True)
        message_file = st.file_uploader('', type=['png', 'jpg', 'bmp'], key="message")
        if message_file is not None:
            message = Image.open(message_file)

            # Check if the message image is in CMYK format
            if message.mode == 'CMYK':
                # Convert the message image to RGB format
                message = message.convert('RGB')

            # Resize the cover image to match the message image size
            cover = resize_image(cover, message)

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
            st.image(stego, caption='This is your stego image')

            # Now add message image and cover image
            stego = coverzero + messageshift

            # Convert the stego array back to an image
            stego_img = Image.fromarray(stego.astype(np.uint8))

            # Add a download link for the stego image
            st.markdown(get_image_download_link(stego_img, 'stego.png', 'Download Stego Image'), unsafe_allow_html=True)