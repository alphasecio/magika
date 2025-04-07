import os, tempfile, mimetypes
import magika, streamlit as st
from pathlib import Path

m = magika.Magika()

# Streamlit app config
st.set_page_config(page_title="Magika Content-Type Scanner")
st.subheader("🔍 Magika Content-Type Scanner")
st.caption("Google's deep learning-based tool for identifying file content types.")

source_file = st.file_uploader("Source File", label_visibility="collapsed")

def get_filetype_icon(label):
    if "image" in label:
        return "🖼️"
    elif "script" in label or "code" in label or "text/x" in label:
        return "🧾"
    elif "pdf" in label or "doc" in label or "text/plain" in label:
        return "📄"
    elif "audio" in label:
        return "🎵"
    elif "video" in label:
        return "🎞️"
    elif "zip" in label or "compressed" in label:
        return "📦"
    else:
        return "📁"

if source_file:
  try:
    # Save uploaded file temporarily to disk, pass the file path to Magika, delete the temp file
    file_bytes = source_file.read()
    file_ext = os.path.splitext(source_file.name)[-1].lower().strip(".")
    mime_from_ext, _ = mimetypes.guess_type(source_file.name)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_bytes)
    result = m.identify_path(Path(tmp_file.name))

    if result.ok:
        detected_type = result.output.label
        description = result.output.description
        confidence = "{:.2f}%".format(result.score * 100)
        icon = get_filetype_icon(detected_type)

        col1, col2 = st.columns(2)

        col1.markdown(f"**File detection (with Magika):**")
        col1.code(
            f"Name: {source_file.name}\n\n"
            f"Type: {detected_type} {icon}\n\n"
            f"Description: {description}\n\n"
            f"Confidence: {confidence}"
        )
        
        col2.markdown("**File metadata (from browser):**")
        col2.code(
            f"Name: {source_file.name}\n\n"
            f"Size: {len(file_bytes)} bytes\n\n"
            f"Extension: .{file_ext}\n\n"
            f"Inferred MIME from extension: {mime_from_ext or 'unknown'}"
        )

    else:
        st.error(f"Magika failed with status: {result.status}")
  except Exception as e:
      st.exception(f"An error occurred: {e}")
  finally:
      os.remove(tmp_file.name)
