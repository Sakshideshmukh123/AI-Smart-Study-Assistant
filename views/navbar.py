"""
Top navigation bar & application header component.
"""

import streamlit as st
from config import APP_VERSION, GITHUB_REPO_URL
from services.gemini_service import GeminiService


def render_navbar() -> str:
    """
    Renders the modern top navigation header bar with brand identity,
    horizontal navigation menu, and API connection status.
    
    Returns:
        str: Selected active page name.
    """
    col_logo, col_nav, col_status = st.columns([2.5, 6.2, 2.3], vertical_alignment="center")

    with col_logo:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div class="brand-text">
                <div class="brand-icon-sq">🎓</div>
                ExamPrep<span>AI</span>
            </div>
            <span class="header-tag-pill">{APP_VERSION}</span>
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

        col_key, col_git = st.columns([3, 1], vertical_alignment="center")
        with col_key:
            with st.popover(status_label, use_container_width=True):
                st.markdown("#### **Google Gemini API Key**")
                st.caption("Connect your key for instant model answers and visual timetables.")

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
                    st.success("✅ Google Gemini connected & active.")
                else:
                    st.info("Don't have a key? [Get free key at Google AI Studio](https://aistudio.google.com/apikey)")

        with col_git:
            st.markdown(
                f'<a href="{GITHUB_REPO_URL}" target="_blank" title="View Source on GitHub" '
                f'style="display: flex; align-items: center; justify-content: center; height: 38px; width: 38px; '
                f'background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 50%; color: #0F172A; '
                f'text-decoration: none; font-size: 1.1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">'
                f'🐙</a>',
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    return selected_page
