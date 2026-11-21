"""
Top navigation bar component with brand logo, horizontal navigation tabs, and API key popover.
"""

import os
import streamlit as st
from services.gemini_service import GeminiService


def render_navbar() -> str:
    """
    Renders the modern top navigation header.
    
    Returns:
        str: Selected active page name.
    """
    col_logo, col_nav, col_status = st.columns([2.5, 6.5, 2.0], vertical_alignment="center")

    with col_logo:
        st.markdown("""
        <div class="brand-text">
            <div class="brand-icon-sq">🎓</div>
            ExamPrep<span>AI</span>
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        nav_options = ["Home", "Study Library", "PYQ Trends", "Answer Studio", "Study Planner"]
        selected_page = st.segmented_control(
            "Navigation",
            options=nav_options,
            default="Home",
            label_visibility="collapsed"
        ) or "Home"

    with col_status:
        gemini = GeminiService(st.session_state.api_key)
        has_key = gemini.is_connected
        status_label = "⚡ AI Connected" if has_key else "🔑 Setup API Key"

        with st.popover(status_label, use_container_width=True):
            st.markdown("#### **Google Gemini API Key**")
            st.caption("Required for model answers and automated study timetable.")

            entered_key = st.text_input(
                "API Key",
                value=st.session_state.api_key,
                type="password",
                placeholder="Paste Gemini API key...",
                label_visibility="collapsed"
            )

            if entered_key != st.session_state.api_key:
                st.session_state.api_key = entered_key
                st.rerun()

            if has_key:
                st.success("✅ Google Gemini active & connected.")
            else:
                st.info("No key? [Get free key at Google AI Studio](https://aistudio.google.com/apikey)")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    return selected_page
