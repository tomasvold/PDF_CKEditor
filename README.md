# PDF to CKEditor Converter 📝

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pdf-ckeditor.streamlit.app/)

A simple tool to convert PDF contracts into clean, editor-ready HTML tables. This is designed to help move content from PDF files into CKEditor4 (or other rich text editors) while preserving table structures and bold formatting.

## 🔗 [Launch the App](https://pdf-ckeditor.streamlit.app/)

## How it works
1. **Upload** a PDF contract.
2. The app uses `pdfplumber` to extract text and tables.
3. It generates **clean HTML** optimized for copy-pasting into source views.
4. **Download** the result or copy the code directly.

## Running Locally
To run this app on your own machine:

```bash
pip install -r requirements.txt
streamlit run app.py
