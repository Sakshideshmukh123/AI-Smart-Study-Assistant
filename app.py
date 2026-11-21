"""
ExamPrep AI — Smart University Exam Preparation Platform
Main Application Orchestrator
"""

import streamlit as st
from config import APP_NAME, APP_ICON, CUSTOM_CSS
from views.navbar import render_navbar
from views.home_view import render_home_view
from views.library_view import render_library_view
from views.pyq_view import render_pyq_view
from views.answer_view import render_answer_view
from views.planner_view import render_planner_view


def init_session_state():
    """Initializes persistent application session state variables."""
    defaults = {
        "documents": {
            "Syllabus": {},
            "PYQ Papers": {},
            "Faculty Notes": {}
        },
        "pyq_results": [],
        "generated_answers": {},
        "study_plan": None,
        "api_key": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    # 1. Page Configuration
    st.set_page_config(
        page_title=f"{APP_NAME} — The Student Exam Planner",
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 2. Inject Design Theme
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # 3. Initialize State
    init_session_state()

    # 4. Top Navigation Bar
    active_view = render_navbar()

    # 5. Route to Active View
    view_routes = {
        "Home": render_home_view,
        "Study Library": render_library_view,
        "PYQ Trends": render_pyq_view,
        "Answer Studio": render_answer_view,
        "Study Planner": render_planner_view
    }

    view_handler = view_routes.get(active_view, render_home_view)
    view_handler()


if __name__ == "__main__":
    main()
