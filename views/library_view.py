"""
Study library management view (PDF uploads and previews).
"""

import streamlit as st
from services.pdf_parser import extract_pdf_pages


def render_library_view():
    """Renders file upload dropzones for Syllabus, PYQ Papers, and Faculty Notes."""
    st.markdown("### **📂 Study Materials Library**")
    st.caption("Upload your syllabus, past year exam papers, and class notes.")

    tab1, tab2, tab3 = st.tabs(["📝 PYQ Papers (Exam Papers)", "📄 Syllabus Outline", "📚 Faculty Notes"])

    sections = [
        (tab1, "PYQ Papers", "Upload past question papers (e.g. 2021, 2022, 2023, 2024) to calculate question frequency."),
        (tab2, "Syllabus", "Upload the official subject syllabus to align topics and modules."),
        (tab3, "Faculty Notes", "Upload lecture presentations and class notes for context-grounded answers.")
    ]

    for tab, cat, tip in sections:
        with tab:
            st.markdown(f"<div class='notice-info'>💡 {tip}</div>", unsafe_allow_html=True)

            files = st.file_uploader(
                f"Choose {cat} PDFs",
                type=["pdf"],
                accept_multiple_files=True,
                key=f"uploader_{cat}"
            )

            if files:
                for f in files:
                    try:
                        text, pages = extract_pdf_pages(f)
                        st.session_state.documents[cat][f.name] = {"text": text, "pages": pages}
                        st.markdown(f"<div class='notice-success'>✅ <b>{f.name}</b> successfully processed ({pages} pages).</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error reading {f.name}: {e}")

            docs = st.session_state.documents[cat]
            if docs:
                st.markdown("<br><b>Uploaded Files:</b>", unsafe_allow_html=True)
                for fname, d in list(docs.items()):
                    r1, r2 = st.columns([5, 1])
                    with r1:
                        st.markdown(f"📄 **{fname}** &nbsp; <small style='color:#64748B;'>({d['pages']} pages)</small>", unsafe_allow_html=True)
                    with r2:
                        if st.button("Delete", key=f"del_{cat}_{fname}"):
                            del st.session_state.documents[cat][fname]
                            st.rerun()
            else:
                st.caption("No files uploaded in this folder.")
