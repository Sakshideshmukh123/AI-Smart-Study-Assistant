"""
Home landing & overview dashboard view.
"""

import streamlit as st


def render_home_view():
    """Renders the main hero banner, key metrics, and feature cards."""
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">A free student planner — built for 100% exam readiness &gt;</div>
        <div class="hero-main-title">
            The free student planner that keeps exam prep <span>organised.</span>
        </div>
        <div class="hero-main-desc">
            Syllabus, question trends, model answers, and revision — planned in one place with your AI study coach, so you're always ahead and on track for your best university grades.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics
    tot_files = sum(len(d) for d in st.session_state.documents.values())
    pyq_count = len(st.session_state.documents["PYQ Papers"])
    extracted_q_count = len(st.session_state.pyq_results)
    has_plan = "Ready" if st.session_state.study_plan else "Not Set"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-box-clean">
            <div class="metric-big-num">{tot_files}</div>
            <div class="metric-sub-label">Course Documents</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box-clean">
            <div class="metric-big-num">{pyq_count}</div>
            <div class="metric-sub-label">Past Year Papers</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-box-clean">
            <div class="metric-big-num">{extracted_q_count}</div>
            <div class="metric-sub-label">Analyzed Questions</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-box-clean">
            <div class="metric-big-num" style="font-size:2.0rem;">{has_plan}</div>
            <div class="metric-sub-label">Revision Timetable</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Value Highlights
    st.markdown("### **Everything you need for exam day**")
    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="card-saas">
            <div class="card-saas-title">🔍 PYQ Repetition Trends</div>
            <div class="card-saas-desc">
                Identify repeating patterns across past papers. Prioritize questions that frequently reappear in university evaluations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="card-saas">
            <div class="card-saas-title">✍️ Model Answers in PDF</div>
            <div class="card-saas-desc">
                Generate high-scoring answers calibrated for 2, 5, or 10 marks. Download ready-to-print, beautifully formatted A4 PDFs.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="card-saas">
            <div class="card-saas-title">📅 Visual Study Schedule</div>
            <div class="card-saas-desc">
                Input your exam date and subjects. Generates an aesthetic timetable image for your phone lockscreen and printable PDF calendar.
            </div>
        </div>
        """, unsafe_allow_html=True)
