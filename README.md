# HDR QC App (with Dynamic File Upload and Image Rating)

This app allows you to upload one or more HDR images, performs basic QC (quality control) analysis, displays histograms, and lets you rate each image.  
Runs in your browser using [Streamlit](https://streamlit.io/).

---

## 1. Requirements

- Python 3.8+
- Pip

---

## 2. Installation

1. **Unzip this folder** to a location of your choice.
2. Open a terminal (command prompt) in the folder.
3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## 3. Running the App

Start the Streamlit app with:

```bash
streamlit run hdr_qc_app.py
```

A browser window will open (if not, go to [http://localhost:8501](http://localhost:8501)).

---

## 4. Usage

1. Upload HDR images (`.hdr`, `.exr`, `.tiff`, `.png`, `.jpg`, etc.).
2. For each image:
    - See basic QC stats (bit depth, luminance, etc.).
    - View the luminance histogram.
    - Rate each image from 1 (Bad) to 5 (Excellent).
3. Your ratings for all images are shown at the bottom.

---

## 5. Notes

- HDR images are best in `.hdr` or `.exr` formats.
- Ratings are not saved—refreshing the page clears them.
- All work is done locally; nothing is uploaded to the cloud.