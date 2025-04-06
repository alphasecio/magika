import os, tempfile
import magika, streamlit as st
from pathlib import Path

m = magika.Magika()

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
    result = m.identify_path(Path(tmp_file.name))

    if result.ok:
        confidence = "{:.2f}%".format(result.score * 100)
        st.success(
            f"**File name**: {source_file.name}\n\n"
            f"**File type**: {result.output.label}\n\n"
            f"**Description**: {result.output.description}\n\n"
            f"**Confidence**: {confidence}")
    else:
        st.error(f"Magika failed with status: {result.status}")
  except Exception as e:
      st.exception(f"An error occurred: {e}")
  
  finally:
      os.remove(tmp_file.name)
