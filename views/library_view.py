"""
Study library management view with 1-Click Sample Dataset Loader and PDF uploads.
"""

import os
import streamlit as st
from services.pdf_parser import extract_pdf_pages


SAMPLE_FILES = {
    "Syllabus": [
        ("sample_data/Syllabus_Machine_Learning.pdf", "Syllabus_Machine_Learning.pdf")
    ],
    "Faculty Notes": [
        ("sample_data/Faculty_Notes_Machine_Learning.pdf", "Faculty_Notes_Machine_Learning.pdf")
    ],
    "PYQ Papers": [
        ("sample_data/PYQ_Paper_May_2022.pdf", "PYQ_Paper_May_2022.pdf"),
        ("sample_data/PYQ_Paper_Dec_2023.pdf", "PYQ_Paper_Dec_2023.pdf"),
        ("sample_data/PYQ_Paper_May_2024.pdf", "PYQ_Paper_May_2024.pdf"),
    ]
}


def load_sample_dataset():
    """Loads pre-generated sample university PDFs directly into session state."""
    for category, files in SAMPLE_FILES.items():
        for path, display_name in files:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    text, pages = extract_pdf_pages(f)
                    st.session_state.documents[category][display_name] = {
                        "text": text,
                        "pages": pages
                    }


def render_library_view():
    """Renders file upload dropzones, instant sample loader, and file previews."""
    st.markdown("### **📂 Study Materials Library**")
    st.caption("Upload your syllabus, past year exam papers, and class notes — or load our instant sample dataset.")

    # ── Interactive 1-Click Test Dataset Card ──
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border: 1.5px solid #BAE6FD; border-radius: 18px; padding: 1.4rem 1.6rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span style="background: #0284C7; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">⚡ Instant Demo Data</span>
                    <h4 style="margin: 0.4rem 0 0.2rem 0; color: #0F172A; font-size: 1.15rem;">Test Immediately with Sample University Dataset (CS & ML)</h4>
                    <p style="margin: 0; color: #475569; font-size: 0.9rem;">
                        Includes 1 Syllabus, 1 Faculty Notes document, and 3 Past Year Exam Papers (2022–2024) with recurring questions.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_demo1, col_demo2 = st.columns([2, 4])
        with col_demo1:
            if st.button("🚀 Load Sample Dataset (1-Click)", type="primary", use_container_width=True):
                load_sample_dataset()
                st.success("✅ Sample dataset loaded! Go to **PYQ Trends** to see the repetition analysis.")
                st.rerun()

        with col_demo2:
            with st.expander("📥 Download Sample PDFs to Your Machine"):
                st.caption("You can download and inspect the generated test PDFs:")
                for cat, flist in SAMPLE_FILES.items():
                    for fpath, fname in flist:
                        if os.path.exists(fpath):
                            with open(fpath, "rb") as f_obj:
                                st.download_button(
                                    label=f"📄 Download {fname} ({cat})",
                                    data=f_obj.read(),
                                    file_name=fname,
                                    mime="application/pdf",
                                    key=f"dl_sample_{fname}"
                                )

    st.markdown("---")

    # Clear All Button if documents exist
    total_docs = sum(len(d) for d in st.session_state.documents.values())
    if total_docs > 0:
        c_status, c_clear = st.columns([5, 1.5])
        with c_status:
            st.info(f"📁 **{total_docs} document(s)** currently loaded in your active session.")
        with c_clear:
            if st.button("🗑️ Clear All Files", use_container_width=True):
                st.session_state.documents = {"Syllabus": {}, "PYQ Papers": {}, "Faculty Notes": {}}
                st.session_state.pyq_results = []
                st.session_state.mastered_questions = set()
                st.rerun()

    # ── Upload Tabs ──
    tab1, tab2, tab3 = st.tabs(["📝 PYQ Papers (Exam Papers)", "📄 Syllabus Outline", "📚 Faculty Notes"])

    sections = [
        (tab1, "PYQ Papers", "Upload past question papers (e.g. 2022, 2023, 2024) to calculate question frequency."),
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
