import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import matplotlib.pyplot as plt

def load_hdr_image(file_bytes, filetype):
    file_bytes.seek(0)
    if filetype in ['.hdr', '.exr']:
        file_bytes = np.asarray(bytearray(file_bytes.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
        if img is None:
            st.error('Failed to load HDR image. Format not supported.')
        return img
    else:
        img = Image.open(file_bytes)
        return np.array(img)

def analyze_hdr(img):
    stats = {}
    stats['Shape'] = img.shape
    stats['Type'] = img.dtype
    if img.dtype == np.uint8:
        stats['HDR'] = False
    elif img.dtype in [np.float32, np.float64]:
        stats['HDR'] = True
    else:
        stats['HDR'] = 'Unknown'
    if img.ndim == 3:
        luminance = 0.2126*img[:,:,2] + 0.7152*img[:,:,1] + 0.0722*img[:,:,0]
    else:
        luminance = img
    stats['Luminance Min'] = float(np.min(luminance))
    stats['Luminance Max'] = float(np.max(luminance))
    stats['Luminance Mean'] = float(np.mean(luminance))
    stats['Luminance Std'] = float(np.std(luminance))
    return stats, luminance

def plot_histogram(luminance):
    fig, ax = plt.subplots()
    ax.hist(luminance.ravel(), bins=256, range=(np.min(luminance), np.max(luminance)))
    ax.set_title('Luminance Histogram')
    ax.set_xlabel('Luminance')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

st.title('HDR Image QC with Rating')

uploaded_files = st.file_uploader(
    "Upload one or more HDR images (.hdr, .exr, .tiff, .png, .jpg)", 
    type=['hdr', 'exr', 'tiff', 'tif', 'png', 'jpg', 'jpeg'],
    accept_multiple_files=True
)

if uploaded_files:
    ratings = {}
    for uploaded_file in uploaded_files:
        st.header(f"Image: {uploaded_file.name}")
        filetype = '.' + uploaded_file.name.split('.')[-1].lower()
        img = load_hdr_image(uploaded_file, filetype)
        if img is not None:
            if img.dtype in [np.float32, np.float64]:
                # Normalize for display
                disp_img = np.clip(img / np.max(img), 0, 1)
                disp_img = (disp_img * 255).astype(np.uint8)
            else:
                disp_img = img
            if disp_img.ndim == 2:
                st.image(disp_img, caption="Grayscale image", channels="GRAY")
            elif disp_img.shape[2] == 3:
                st.image(disp_img, caption="RGB image", channels="BGR" if filetype in ['.hdr', '.exr'] else "RGB")
            else:
                st.write("Image format not supported for display.")

            stats, luminance = analyze_hdr(img)
            st.write("**QC Stats:**")
            st.json(stats)
            plot_histogram(luminance)
            rating = st.slider(
                f"Rate this image (1 = Bad, 5 = Excellent):", 
                min_value=1, max_value=5, value=3, key=uploaded_file.name
            )
            ratings[uploaded_file.name] = rating
            st.write(f"Your rating: {rating}/5")

    st.write("## All Ratings")
    st.json(ratings)