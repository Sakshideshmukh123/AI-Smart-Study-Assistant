"""
Application footer component — clean, minimalist, and fully responsive.
"""

import streamlit as st
from config import GITHUB_REPO_URL, APP_VERSION


def render_footer():
    """
    Renders a sleek, bug-free, modern SaaS footer at the bottom of the page.
    """
    st.markdown("<div style='height: 3.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    col_left, col_center, col_right = st.columns([4, 4, 3], vertical_alignment="center")

    with col_left:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-weight: 800; font-size: 1.05rem; color: #0F172A;">🎓 ExamPrep<span style="color: #0284C7;">AI</span></span>
                <span style="background: #F1F5F9; border: 1px solid #E2E8F0; color: #475569; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.55rem; border-radius: 9999px;">The Student Exam Planner</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_center:
        st.markdown(
            """
            <div style="text-align: center; font-size: 0.85rem; color: #64748B;">
                Crafted with ❤️ for university & engineering students worldwide.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown(
            f"""
            <div style="text-align: right; font-size: 0.85rem;">
                <a href="{GITHUB_REPO_URL}" target="_blank" style="text-decoration: none; color: #0284C7; font-weight: 700;">
                    🐙 GitHub
                </a>
                <span style="color: #CBD5E1; margin: 0 0.4rem;">•</span>
                <span style="color: #64748B;">MIT License</span>
                <span style="color: #CBD5E1; margin: 0 0.4rem;">•</span>
                <span style="color: #94A3B8;">{APP_VERSION}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
