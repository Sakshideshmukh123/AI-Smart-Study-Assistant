"""
AI Model Answer Studio view with marks calibration and direct PDF export.
"""

from datetime import datetime
import streamlit as st
from services.gemini_service import GeminiService
from services.report_generator import generate_answer_pdf, REPORTLAB_AVAILABLE


def _get_context_summary(max_chars: int = 3500) -> str:
    chunks = []
    for cat, docs in st.session_state.documents.items():
        for name, data in docs.items():
            chunks.append(f"[{cat}: {name}]\n{data['text'][:1500]}")
    return "\n\n".join(chunks)[:max_chars]


def render_answer_view():
    """Renders the question input, mark weightage options, and PDF generation."""
    st.markdown("### **✍️ AI Exam Answer Studio**")
    st.caption("Generate structured, high-scoring university answers and export them directly to PDF.")

    preset_q = st.session_state.pop("target_question", "")

    question_text = st.text_area(
        "Exam Question:",
        value=preset_q,
        height=90,
        placeholder="e.g. Explain the difference between Supervised and Unsupervised Learning with suitable diagrams and examples."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        marks_selected = st.selectbox(
            "Exam Mark Weightage:",
            ["2 Marks (Brief & Precise)", "5 Marks (Standard with Points)", "10 Marks (Comprehensive Essay)"],
            index=2
        )
    with c2:
        source_context = st.selectbox(
            "Information Source:",
            ["Gemini Knowledge Base", "Uploaded Study Materials", "Combined (Recommended)"],
            index=2
        )
    with c3:
        subject_name = st.text_input("Subject / Module Name:", placeholder="e.g. Machine Learning")

    generate_btn = st.button("✨ Generate Exam Answer", type="primary", use_container_width=True)

    if generate_btn and question_text.strip():
        gemini = GeminiService(st.session_state.api_key)
        if not gemini.is_connected:
            st.warning("⚠️ Please configure your Gemini API key in the top right menu.")
            return

        ctx = ""
        if "Materials" in source_context or "Combined" in source_context:
            ctx = _get_context_summary()

        system_instruction = (
            "You are a top university exam professor. Format answers with clear section headings, "
            "bold key terminology, bulleted explanations, and summary points. "
            f"Tailor the depth strictly to a {marks_selected} standard."
        )

        user_prompt = f"Question: {question_text}\nMarks: {marks_selected}\nSubject: {subject_name or 'General'}"
        if ctx:
            user_prompt += f"\n\nReference Material:\n{ctx}"

        with st.spinner("Writing model answer..."):
            answer = gemini.ask(user_prompt, system=system_instruction)

        st.session_state.generated_answers[question_text] = {
            "answer": answer,
            "marks": marks_selected,
            "subject": subject_name
        }

    # Render Answer & Download PDF
    if question_text in st.session_state.generated_answers:
        data = st.session_state.generated_answers[question_text]
        st.markdown(f"""
        <div class="model-answer-view">
            <h4 style="color:#0284C7;margin-top:0;">Model Answer ({data['marks']})</h4>
            {data['answer']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if REPORTLAB_AVAILABLE:
            pdf_bytes = generate_answer_pdf(
                question=question_text,
                answer=data["answer"],
                marks=data["marks"].split()[0],
                subject=data["subject"]
            )
            st.download_button(
                label="📥 Download Answer as PDF",
                data=pdf_bytes,
                file_name=f"ExamAnswer_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("ReportLab library not installed. PDF generation unavailable.")
