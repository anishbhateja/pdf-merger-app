import streamlit as st
from PIL import Image
from PyPDF2 import PdfMerger
import tempfile
import os

st.title("📄 Merge PDFs & Images to Single PDF 🐻‍❄️ Edition: Anish Bhateja")

uploaded_files = st.file_uploader("Upload PDFs or Images", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Merge Files"):
        merger = PdfMerger()
        temp_files = []

        for file in uploaded_files:
            file_type = file.name.lower().split(".")[-1]

            if file_type == "pdf":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    temp_files.append(tmp.name)
                    merger.append(tmp.name)

            elif file_type in ["jpg", "jpeg", "png"]:
                image = Image.open(file).convert("RGB")
                img_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                image.save(img_temp.name)
                temp_files.append(img_temp.name)
                merger.append(img_temp.name)

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        merger.write(output_path.name)
        merger.close()

        with open(output_path.name, "rb") as f:
            st.download_button("📥 Download Merged PDF", f.read(), file_name="merged_output.pdf", mime="application/pdf")

        # Cleanup
        for t in temp_files:
            os.remove(t)
        os.remove(output_path.name)
