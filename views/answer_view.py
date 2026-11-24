"""
AI Model Answer Studio view with marks calibration, academic rubrics, and direct PDF export.
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
    """Renders the question input, mark weightage options, academic rubrics, and PDF generation."""
    st.markdown("### **✍️ AI Exam Answer Studio**")
    st.caption("Generate structured, university-rubric answers calibrated by marks with direct A4 PDF export.")

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
            ["Combined (Recommended)", "Uploaded Study Materials", "Gemini Knowledge Base"],
            index=0
        )
    with c3:
        subject_name = st.text_input("Subject / Module Name:", placeholder="e.g. Machine Learning")

    # ── Interactive Academic Rubric Toggles (Why this beats raw ChatGPT) ──
    st.markdown("**🎯 University Scoring Boosters (Choose what to inject):**")
    r1, r2, r3 = st.columns(3)
    with r1:
        inc_rubric = st.checkbox("📊 Marking Scheme Breakdown", value=True, help="Shows how marks are allocated by university evaluators.")
    with r2:
        inc_mnemonic = st.checkbox("💡 Mnemonic / Memory Hook", value=True, help="Provides an easy acronym to remember all points in the exam hall.")
    with r3:
        inc_pitfalls = st.checkbox("⚠️ Pitfalls & Common Mistakes", value=True, help="Highlights frequent misconceptions where students lose marks.")

    generate_btn = st.button("✨ Generate Model Answer", type="primary", use_container_width=True)

    if generate_btn and question_text.strip():
        gemini = GeminiService(st.session_state.api_key)
        if not gemini.is_connected:
            st.warning("⚠️ Please configure your Gemini API key in the top right menu.")
            return

        ctx = ""
        if "Materials" in source_context or "Combined" in source_context:
            ctx = _get_context_summary()

        system_instruction = (
            "You are a strict, experienced university professor and chief examiner. "
            "Write a high-scoring, structured exam answer formatted strictly for university papers. "
            "Use clear headings, bold keywords, numbered formulas, and bullet points. "
            f"Tailor the depth strictly to the {marks_selected} standard."
        )

        user_prompt = f"Question: {question_text}\nMarks: {marks_selected}\nSubject: {subject_name or 'General'}"
        if ctx:
            user_prompt += f"\n\nReference Material from Course Notes & Syllabus:\n{ctx}"

        if inc_rubric:
            user_prompt += "\n\nInclude a section: '## 📋 Evaluator Marking Scheme' detailing marks distribution."
        if inc_mnemonic:
            user_prompt += "\n\nInclude a section: '## 💡 Exam Hall Memory Trick' with a memorable acronym or mnemonic."
        if inc_pitfalls:
            user_prompt += "\n\nInclude a section: '## ⚠️ Common Mistakes to Avoid' pointing out where students lose marks."

        with st.spinner("Drafting professor-grade model answer..."):
            answer = gemini.ask(user_prompt, system=system_instruction)

        st.session_state.generated_answers[question_text] = {
            "answer": answer,
            "marks": marks_selected,
            "subject": subject_name
        }

    # Render Answer, PDF Download & Self-Assessment Rubric
    if question_text in st.session_state.generated_answers:
        data = st.session_state.generated_answers[question_text]
        st.markdown(f"""
        <div class="model-answer-view">
            <h4 style="color:#0284C7;margin-top:0;">Model Answer ({data['marks']})</h4>
            {data['answer']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # PDF Download Button
        col_pdf, col_mark = st.columns([2, 3])
        with col_pdf:
            if REPORTLAB_AVAILABLE:
                pdf_bytes = generate_answer_pdf(
                    question=question_text,
                    answer=data["answer"],
                    marks=data["marks"].split()[0],
                    subject=data["subject"]
                )
                st.download_button(
                    label="📥 Download Model Answer as PDF",
                    data=pdf_bytes,
                    file_name=f"ExamAnswer_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning("ReportLab library not installed. PDF generation unavailable.")

        with col_mark:
            is_mastered = question_text in st.session_state.mastered_questions
            if st.button("✅ Mark as Mastered for Exam" if not is_mastered else "🎉 Already in Mastered List", use_container_width=True):
                st.session_state.mastered_questions.add(question_text)
                st.success("Added to your Mastered Questions list! Check the Readiness Meter in PYQ Trends.")

        # Interactive Self-Assessment Checklist (Active Recall)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📝 Student Self-Assessment Checklist (Test Your Recall)", expanded=True):
            st.caption("Check off items as you practice writing this answer on paper:")
            st.checkbox("1. Did I state the formal definition with exact technical terms?", key=f"sa_1_{question_text[:20]}")
            st.checkbox("2. Did I sketch the architecture/flowchart or block diagram?", key=f"sa_2_{question_text[:20]}")
            st.checkbox("3. Did I write at least 4-5 distinct sub-headed points?", key=f"sa_3_{question_text[:20]}")
            st.checkbox("4. Did I give at least one concrete real-world application?", key=f"sa_4_{question_text[:20]}")
            st.checkbox("5. Did I mention time complexity, cost function, or formula?", key=f"sa_5_{question_text[:20]}")
