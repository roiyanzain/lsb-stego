import streamlit as st

def readmePage():
    st.header(':warning: DISCLAIMER')
    st.write('1. This program only accept encrypting image with same size (example : the cover has 300x300 px, then the message image should 300x300 px)')
    st.write('2. This program only accept CMYK image. If you want to encrypt RGB image, you should convert it to CMYK first')
    st.write('3. The result image will be saved as the TIFF format, because the format can store CMYK color mode.')