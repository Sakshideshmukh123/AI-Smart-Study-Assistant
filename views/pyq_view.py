"""
Previous Year Questions (PYQ) repetition analysis view with Interactive Exam Mastery Tracker.
"""

import streamlit as st
from services.pyq_engine import run_pyq_analysis


# Built-in quick recall summaries for high-frequency patterns
QUICK_RECALL_TIPS = {
    "supervised": "• Labeled input-output data pairs\n• Goal: Map X → Y function\n• Key algorithms: Linear Regression, Logistic Regression, SVM, Decision Trees\n• Real-world use: Spam detection, house price prediction",
    "k-means": "• Unsupervised centroid-based clustering\n• 4 steps: 1) Pick K centroids, 2) Assign points to nearest centroid (Euclidean distance), 3) Recompute centroid mean, 4) Repeat until convergence\n• Optimal K: Elbow method (SSE vs K)",
    "overfitting": "• Model memorizes training noise and fails to generalize (High Variance, Low Bias)\n• Mitigation: L1 (Lasso)/L2 (Ridge) Regularization, Dropout, Early Stopping, Pruning, Data Augmentation",
    "decision tree": "• Hierarchical model splitting on attribute with maximum Information Gain\n• Entropy H(S) = -Σ p*log2(p)\n• Information Gain = H(Parent) - Σ Weighted H(Children)\n• Pruning removes insignificant subtrees to combat overfitting",
    "confusion matrix": "• Performance table: TP, TN, FP, FN\n• Precision = TP / (TP + FP) (Quality of positive predictions)\n• Recall (Sensitivity) = TP / (TP + FN) (Completeness of detection)\n• F1-Score = 2 * (Precision * Recall) / (Precision + Recall)",
    "svm": "• Finds optimal hyperplane with Maximum Margin between classes\n• Support Vectors: data points closest to decision boundary\n• Kernel Trick: maps non-linear data to higher dimensions (RBF, Polynomial)",
}


def get_quick_recall_tip(question_text: str) -> str:
    """Returns a 60-second active recall bullet summary based on question keywords."""
    q_lower = question_text.lower()
    for key, tip in QUICK_RECALL_TIPS.items():
        if key in q_lower:
            return tip
    return (
        "• State formal technical definition first\n"
        "• Draw a quick 3-block diagram/architecture\n"
        "• Mention 2 industry real-world use cases\n"
        "• State mathematical formula/cost function if applicable"
    )


def render_pyq_view():
    """Renders question extraction, repetition filtering, and interactive mastery tracking."""
    st.markdown("### **🔍 Past Year Question (PYQ) Trends & Exam Mastery**")
    st.caption("Pinpoint repeated questions across multiple university papers and track your mastery.")

    pyq_docs = st.session_state.documents["PYQ Papers"]
    n_papers = len(pyq_docs)

    if n_papers == 0:
        st.markdown(
            """
            <div class='notice-info'>
            ⚠️ No exam papers uploaded yet.<br/>
            Go to <b>📂 Study Library</b> and click <b>🚀 Load Sample Dataset (1-Click)</b> to instantly test with 3 past papers!
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Auto-run analysis if not yet run
    if not st.session_state.pyq_results:
        with st.spinner("Analyzing question papers..."):
            st.session_state.pyq_results = run_pyq_analysis(pyq_docs)

    results = st.session_state.pyq_results

    # ── Interactive Gamified Exam Readiness Header ──
    total_q = len(results)
    mastered_count = len(st.session_state.mastered_questions)
    readiness_pct = int((mastered_count / total_q) * 100) if total_q > 0 else 0

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 18px; padding: 1.25rem 1.6rem; margin-bottom: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
            <div>
                <span style="font-size: 0.82rem; font-weight: 700; color: #0284C7; text-transform: uppercase; letter-spacing: 0.5px;">🎯 Exam Readiness Meter</span>
                <h4 style="margin: 0.2rem 0 0 0; color: #0F172A; font-size: 1.25rem;">
                    {mastered_count} of {total_q} Questions Mastered ({readiness_pct}% Prepared)
                </h4>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 1.6rem; font-weight: 800; color: {'#059669' if readiness_pct >= 60 else '#0284C7'};">
                    {readiness_pct}%
                </span>
            </div>
        </div>
        <div style="background: #E2E8F0; border-radius: 9999px; height: 10px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #0284C7, #38BDF8); height: 100%; width: {readiness_pct}%; border-radius: 9999px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter Controls
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
        if st.button("🔄 Re-run Analysis", use_container_width=True):
            with st.spinner("Re-analyzing question papers..."):
                st.session_state.pyq_results = run_pyq_analysis(pyq_docs)
            st.rerun()

    filtered_results = [r for r in results if r["frequency"] >= min_freq]
    st.markdown(f"#### **Showing {len(filtered_results)} High-Yield Question(s)**")

    for idx, item in enumerate(filtered_results, 1):
        freq = item["frequency"]
        q_text = item["question"]
        is_mastered = q_text in st.session_state.mastered_questions

        if freq >= 3:
            badge = "<span class='badge-priority badge-high'>🔥 High Priority (Repeated 3+ Years)</span>"
        elif freq == 2:
            badge = "<span class='badge-priority badge-medium'>⚡ Medium Priority (Repeated 2 Years)</span>"
        else:
            badge = "<span class='badge-priority badge-low'>Standard (Appeared 1 Year)</span>"

        st.markdown(f"""
        <div class="question-item-card" style="border-left-color: {'#059669' if is_mastered else '#0284C7'};">
            <div style="margin-bottom:0.4rem; display: flex; justify-content: space-between; align-items: center;">
                <div>{badge} &nbsp; <small style="color:#64748B;">Appeared in {freq} of {item['total']} papers</small></div>
                <div>{'<span style="color:#059669; font-weight:700; font-size:0.85rem;">✅ Mastered</span>' if is_mastered else '<span style="color:#64748B; font-size:0.82rem;">⏳ Revision Pending</span>'}</div>
            </div>
            <div style="font-weight:600;font-size:1.05rem;color:#0F172A;">{idx}. {q_text}</div>
            <div style="font-size:0.83rem;color:#64748B;margin-top:0.45rem;">📄 Found in: {', '.join(item['appeared_in'])}</div>
        </div>
        """, unsafe_allow_html=True)

        col_act1, col_act2, col_act3 = st.columns([1.5, 2.5, 3])
        with col_act1:
            # Interactive Mastery Checkbox
            checked = st.checkbox("Mark as Mastered", value=is_mastered, key=f"chk_master_{idx}")
            if checked != is_mastered:
                if checked:
                    st.session_state.mastered_questions.add(q_text)
                else:
                    st.session_state.mastered_questions.discard(q_text)
                st.rerun()

        with col_act2:
            # Send to Answer Studio
            if st.button("✍️ Generate Model Answer", key=f"quick_ans_{idx}"):
                st.session_state["target_question"] = q_text
                st.info("Question transferred! Go to **Answer Studio** from the top bar to customize marks & download PDF.")

        with col_act3:
            # Interactive Flashcard Active Recall
            with st.expander("⚡ 60-Sec Active Recall Flashcard"):
                st.markdown("**Key Exam Concepts to Recall:**")
                st.markdown(get_quick_recall_tip(q_text))
