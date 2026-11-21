"""
Previous Year Questions (PYQ) repetition analysis view.
"""

import streamlit as st
from services.pyq_engine import run_pyq_analysis


def render_pyq_view():
    """Renders question extraction, repetition filtering, and priority badges."""
    st.markdown("### **🔍 Past Year Question (PYQ) Trends**")
    st.caption("Pinpoint repeated questions across multiple university papers.")

    pyq_docs = st.session_state.documents["PYQ Papers"]
    n_papers = len(pyq_docs)

    if n_papers == 0:
        st.markdown(
            "<div class='notice-info'>⚠️ Please upload past exam papers in <b>📂 Study Library → PYQ Papers</b> first.</div>",
            unsafe_allow_html=True
        )
        return

    c_left, c_right = st.columns([3, 1])
    with c_left:
        min_freq = st.slider(
            "Filter: Show questions appearing in at least:",
            min_value=1,
            max_value=max(2, n_papers),
            value=min(2, n_papers),
            format="%d paper(s)"
        )
    with c_right:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_clicked = st.button("🔍 Run Trends Analysis", use_container_width=True)

    if analyze_clicked:
        with st.spinner("Analyzing question papers..."):
            st.session_state.pyq_results = run_pyq_analysis(pyq_docs)
        st.success(f"Extracted {len(st.session_state.pyq_results)} unique questions from {n_papers} paper(s)!")

    if st.session_state.pyq_results:
        results = [r for r in st.session_state.pyq_results if r["frequency"] >= min_freq]
        st.markdown(f"#### **Found {len(results)} Question(s)**")

        for idx, item in enumerate(results, 1):
            freq = item["frequency"]
            if freq >= 3:
                badge = "<span class='badge-priority badge-high'>🔥 High Priority</span>"
            elif freq == 2:
                badge = "<span class='badge-priority badge-medium'>⚡ Medium Priority</span>"
            else:
                badge = "<span class='badge-priority badge-low'>Regular</span>"

            st.markdown(f"""
            <div class="question-item-card">
                <div style="margin-bottom:0.4rem;">{badge} &nbsp; <small style="color:#64748B;">Appeared in {freq} of {item['total']} papers</small></div>
                <div style="font-weight:600;font-size:1.05rem;color:#0F172A;">{idx}. {item['question']}</div>
                <div style="font-size:0.83rem;color:#64748B;margin-top:0.45rem;">📄 Found in: {', '.join(item['appeared_in'])}</div>
            </div>
            """, unsafe_allow_html=True)

            col_btn, _ = st.columns([2.5, 5])
            with col_btn:
                if st.button("Generate Model Answer", key=f"quick_ans_{idx}"):
                    st.session_state["target_question"] = item["question"]
                    st.info("Question loaded! Go to **Answer Studio** from the top navigation bar to generate.")
