import streamlit as st
import ezdxf
import tempfile
import os

def remove_hatches(doc):
    for layout in doc.layouts:
        for hatch in list(layout.query('HATCH')):
            layout.delete_entity(hatch)

def process_dxf(uploaded_file):
    # Write uploaded bytes into temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp_in:
        tmp_in.write(uploaded_file.getbuffer())
        tmp_in.flush()
        tmp_in_name = tmp_in.name
    
    # Load DXF
    doc = ezdxf.readfile(tmp_in_name)
    remove_hatches(doc)
    
    # Write to a temp output file
    out_path = tmp_in_name.replace(".dxf", "_no_hatch.dxf")
    doc.saveas(out_path)
    
    # Read bytes to return
    with open(out_path, "rb") as f:
        out_bytes = f.read()
    
    # Clean up temp files
    try:
        os.remove(tmp_in_name)
        os.remove(out_path)
    except Exception:
        pass
    
    return out_bytes, os.path.basename(out_path)

def main():
    st.title("DXF Hatch Remover")
    uploaded_file = st.file_uploader("Upload a DXF file", type=["dxf"])
    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")
        with st.spinner("Processing…"):
            out_bytes, out_name = process_dxf(uploaded_file)
        st.success("Done. Download below:")
        st.download_button(
            label="Download cleaned DXF",
            data=out_bytes,
            file_name=out_name,
            mime="application/dxf"
        )

if __name__ == "__main__":
    main()
