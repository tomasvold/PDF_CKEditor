import streamlit as st
import pdfplumber
import io

# -- CORE CONVERSION LOGIC (Same as your local script) --
def get_ckeditor_content(objs):
    if not objs:
        return "&nbsp;"
    parts = []
    for obj in objs:
        text = obj.get("text", "")
        if text in ["☐", "□"]:
            parts.append("☐ ")
            continue
        font_name = obj.get("fontname", "").lower()
        is_bold = any(kw in font_name for kw in ["bold", "black", "heavy", "700"])
        content = text
        if is_bold:
            content = f"<strong>{content}</strong>"
        parts.append(content)
    return "".join(parts).replace("\n", " ")

# -- STREAMLIT UI --
st.set_page_config(page_title="Contract PDF Converter", page_icon="📝")
st.title("📄 PDF to CKEditor Converter")
st.write("Upload a contract PDF to generate editor-ready tables.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Streamlit returns a BytesIO object, which pdfplumber can read directly
    with pdfplumber.open(uploaded_file) as pdf:
        full_html = "<html><body>"
       
        for i, page in enumerate(pdf.pages):
            full_html += f"<p><strong>PAGE {i+1}</strong></p>"
           
            tables = page.find_tables(table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 4,
            })

            if tables:
                for table in tables:
                    full_html += '<table border="1" cellspacing="0" cellpadding="5" style="width:100%; border-collapse: collapse;">'
                    for row in table.rows:
                        full_html += "<tr>"
                        for cell in row.cells:
                            if cell:
                                cell_area = page.crop(cell)
                                cell_content = get_ckeditor_content(cell_area.chars)
                                full_html += f'<td style="vertical-align: top; border: 1px solid #000;">{cell_content}</td>'
                            else:
                                full_html += "<td>&nbsp;</td>"
                        full_html += "</tr>"
                    full_html += "</table><br>"
            else:
                text = page.extract_text()
                if text:
                    clean_text = text.replace('\n', '<br>')
                    full_html += f"<p>{clean_text}</p>"
            full_html += "<hr>"
        full_html += "</body></html>"

    # 1. Preview Area
    st.subheader("Visual Preview")
    st.html(full_html)

    # 2. Copy/Paste Area
    st.subheader("HTML Source Code")
    st.text_area("Copy this code and paste it into the editor's Source view:", value=full_html, height=300)

    # 3. Download Button
    st.download_button(
        label="Download HTML File",
        data=full_html,
        file_name="contract_for_editor.html",
        mime="text/html"
    )
