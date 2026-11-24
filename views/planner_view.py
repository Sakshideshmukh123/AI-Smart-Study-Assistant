"""
Visual study planner view (Timetable Image + A4 PDF export) with interactive subject autofill.
"""

import re
import json
from datetime import datetime, timedelta
import streamlit as st
from services.gemini_service import GeminiService
from services.report_generator import generate_plan_pdf, REPORTLAB_AVAILABLE
from services.visualizer import generate_schedule_image, MATPLOTLIB_AVAILABLE


def render_planner_view():
    """Renders the study planner form, generated schedule table, visual image card, and PDF."""
    st.markdown("### **📅 Visual Study Planner**")
    st.caption("Generate a structured day-by-day revision schedule with a phone-friendly visual image and A4 PDF.")

    # Interactive autofill helper
    default_subjs = ""
    if st.session_state.pyq_results:
        top_topics = [
            "Supervised & Unsupervised Learning",
            "K-Means Clustering & PCA",
            "Decision Trees & Information Gain",
            "Bias-Variance Tradeoff & Regularization",
            "Model Evaluation (Confusion Matrix & ROC)"
        ]
        default_subjs = "\n".join(top_topics)
    elif "Syllabus" in st.session_state.documents and st.session_state.documents["Syllabus"]:
        default_subjs = "Unit 1: Foundations of Machine Learning\nUnit 2: Classification & Decision Trees\nUnit 3: Clustering & Dimensionality Reduction\nUnit 4: Model Evaluation & Ensembles"

    col_btn_fill, _ = st.columns([2.5, 4])
    with col_btn_fill:
        if st.button("✨ Auto-fill Sample CS/ML Modules", help="Quickly populates 4 core university modules for testing."):
            st.session_state["preset_planner_subjs"] = (
                "Supervised & Unsupervised Learning\n"
                "K-Means Clustering & PCA\n"
                "Decision Trees & Regularization\n"
                "Model Evaluation Metrics"
            )
            st.rerun()

    preset_val = st.session_state.pop("preset_planner_subjs", default_subjs or "Data Mining\nMachine Learning\nDatabase Systems\nComputer Networks")

    with st.form("study_plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            exam_date_val = st.date_input(
                "Target Exam Date:",
                value=datetime.today().date() + timedelta(days=14),
                min_value=datetime.today().date() + timedelta(days=1)
            )
            daily_hours_val = st.slider("Daily Study Availability (Hours):", 1, 10, 4)

        with col2:
            subjects_input = st.text_area(
                "Subjects / Units to Cover (One per line):",
                value=preset_val,
                height=110
            )

        submit_plan = st.form_submit_button("📅 Build Visual Study Plan", type="primary", use_container_width=True)

    if submit_plan:
        subjs = [s.strip() for s in subjects_input.split("\n") if s.strip()]
        if not subjs:
            st.error("Please provide at least one subject.")
            return

        gemini = GeminiService(st.session_state.api_key)
        if not gemini.is_connected:
            st.warning("⚠️ Please configure your Gemini API key in the top right menu.")
            return

        days_until = (exam_date_val - datetime.today().date()).days

        pyq_summary = ""
        if st.session_state.pyq_results:
            top_qs = [r["question"] for r in st.session_state.pyq_results[:5]]
            pyq_summary = "Incorporate these recurring questions:\n" + "\n".join(f"- {q}" for q in top_qs)

        prompt = f"""Generate a detailed university exam preparation timetable.
Exam Date: {exam_date_val} (In {days_until} days)
Daily Study Hours: {daily_hours_val} hours
Subjects: {', '.join(subjs)}

{pyq_summary}

Requirements:
1. Provide a day-by-day table of revision.
2. Reserve the final 2-3 days for mock practice and revision.
3. Include short study tips.
4. Output a JSON block at the end with this format:
```json
{{
  "schedule": [
    {{"day": 1, "date": "Day 1", "subject": "{subjs[0]}", "hours": {daily_hours_val}, "focus": "Core concepts and definitions"}},
    {{"day": 2, "date": "Day 2", "subject": "{subjs[min(1, len(subjs)-1)]}", "hours": {daily_hours_val}, "focus": "Algorithms and practice"}}
  ]
}}
```
"""
        with st.spinner("Designing your study schedule..."):
            raw_plan = gemini.ask(
                prompt,
                system="You are an expert academic strategist. Return clear, motivating plans with the required JSON block."
            )

        sched_list = []
        json_m = re.search(r"```json\s*(.*?)\s*```", raw_plan, re.DOTALL)
        clean_plan_text = raw_plan
        if json_m:
            try:
                parsed = json.loads(json_m.group(1))
                sched_list = parsed.get("schedule", [])
                clean_plan_text = raw_plan[:json_m.start()].strip()
            except Exception:
                pass

        st.session_state.study_plan = {
            "text": clean_plan_text,
            "schedule": sched_list,
            "exam_date": datetime.combine(exam_date_val, datetime.min.time()),
            "subjects": subjs,
            "days_left": days_until
        }

    # Display Active Plan
    if st.session_state.study_plan:
        plan_obj = st.session_state.study_plan
        st.markdown("<br>", unsafe_allow_html=True)

        t_plan, t_img, t_pdf = st.tabs(["📋 Timetable Overview", "🖼️ Visual Schedule Image", "📄 Download A4 PDF"])

        with t_plan:
            st.markdown(plan_obj["text"])

        with t_img:
            if not MATPLOTLIB_AVAILABLE:
                st.warning("Matplotlib is required for visual image rendering.")
            elif not plan_obj["schedule"]:
                st.info("Visual image not available for this plan. Try re-generating.")
            else:
                img_data = generate_schedule_image(
                    plan_obj["schedule"],
                    exam_date_str=plan_obj["exam_date"].strftime("%d %B %Y")
                )
                if img_data:
                    st.image(img_data, use_container_width=True, caption="Study Timetable Card — ExamPrep AI")
                    st.download_button(
                        label="📥 Download Timetable Image (PNG)",
                        data=img_data,
                        file_name="StudySchedule.png",
                        mime="image/png"
                    )

        with t_pdf:
            if not REPORTLAB_AVAILABLE:
                st.warning("ReportLab is required for PDF export.")
            else:
                pdf_doc = generate_plan_pdf(
                    plan_obj["text"],
                    plan_obj["subjects"],
                    plan_obj["exam_date"],
                    plan_obj["days_left"]
                )
                st.download_button(
                    label="📥 Download Timetable (PDF)",
                    data=pdf_doc,
                    file_name="ExamStudyPlan.pdf",
                    mime="application/pdf"
                )
