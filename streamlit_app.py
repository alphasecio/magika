import os, tempfile, streamlit as st
from pathlib import Path
from magika import Magika
magika = Magika()

# Streamlit app
st.subheader("Magika content-type scanner")
source_file = st.file_uploader("Source File", label_visibility="collapsed")

if not source_file:
  st.error(f"Please upload the file to be classified.")
else:
  try:
    # Save uploaded file temporarily to disk, pass the file path to Magika, delete the temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(source_file.read())
    result = magika.identify_path(Path(tmp_file.name))
    confidence = "{:.2f}%".format(result.output.score * 100)
    st.success(f"File type: {result.output.ct_label}\n\nDescription: {result.output.magic}\n\nConfidence: {confidence}")
    os.remove(tmp_file.name)
  except Exception as e:
    st.exception(f"An error occurred: {e}")
