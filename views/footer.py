"""
Application footer component with brand info, quick navigation, tech stack, and GitHub links.
"""

import streamlit as st
from config import GITHUB_REPO_URL, APP_VERSION


def render_footer():
    """
    Renders a comprehensive, modern SaaS footer at the bottom of the page.
    """
    st.markdown(f"""
    <div class="app-footer-wrapper">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 2rem;">
            <!-- Column 1: Brand & Mission -->
            <div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem;">
                    🎓 ExamPrep<span style="color: #0284C7;">AI</span>
                </div>
                <p style="font-size: 0.88rem; color: #64748B; line-height: 1.6; margin-bottom: 1rem;">
                    The intelligent university exam preparation platform. Built for students to discover recurring question trends, practice active recall, generate marks-calibrated model answers, and plan visual revision schedules.
                </p>
                <div>
                    <span class="footer-tech-tag">Python 3.12</span>
                    <span class="footer-tech-tag">Google Gemini</span>
                    <span class="footer-tech-tag">ReportLab PDF</span>
                    <span class="footer-tech-tag">Streamlit</span>
                </div>
            </div>

            <!-- Column 2: Platform Modules -->
            <div>
                <div class="footer-col-title">Core Modules</div>
                <div class="footer-link-item">🏠 Overview & Metric Dashboard</div>
                <div class="footer-link-item">📂 Study Materials Library</div>
                <div class="footer-link-item">🔍 PYQ Repetition Trend Analyzer</div>
                <div class="footer-link-item">✍️ AI Model Answer Studio</div>
                <div class="footer-link-item">📅 Visual Study Schedule Planner</div>
            </div>

            <!-- Column 3: High-Yield Student Features -->
            <div>
                <div class="footer-col-title">Interactive Tools</div>
                <div class="footer-link-item">⚡ 60-Sec Active Recall Flashcards</div>
                <div class="footer-link-item">🎯 Real-Time Exam Readiness Meter</div>
                <div class="footer-link-item">📋 Evaluator Marking Schemes</div>
                <div class="footer-link-item">💡 Exam Hall Memory Mnemonics</div>
                <div class="footer-link-item">⚠️ Common Pitfalls & Mistakes Guide</div>
            </div>

            <!-- Column 4: Open Source & Developer -->
            <div>
                <div class="footer-col-title">Developer & Project</div>
                <div class="footer-link-item">
                    🐙 <a href="{GITHUB_REPO_URL}" target="_blank">GitHub Repository</a>
                </div>
                <div class="footer-link-item">
                    📄 <a href="{GITHUB_REPO_URL}#readme" target="_blank">Documentation & Architecture</a>
                </div>
                <div class="footer-link-item">
                    ⚖️ License: MIT Open Source
                </div>
                <div class="footer-link-item">
                    👩‍💻 Developed by Sakshi Deshmukh
                </div>
                <div style="margin-top: 0.8rem;">
                    <a href="{GITHUB_REPO_URL}" target="_blank" style="text-decoration: none;">
                        <span style="background: #0284C7; color: white; padding: 0.35rem 0.85rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 700;">
                            ⭐ Star on GitHub
                        </span>
                    </a>
                </div>
            </div>
        </div>

        <!-- Bottom Copyright Row -->
        <div class="footer-bottom-bar">
            <div>
                © 2026 <b>ExamPrep AI</b>. Crafted with ❤️ for university & engineering students worldwide.
            </div>
            <div>
                MIT License &nbsp;•&nbsp; Academic Portfolio Project &nbsp;•&nbsp; {APP_VERSION}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
