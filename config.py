"""
Application configuration and styling constants for ExamPrep AI.
"""

# App branding
APP_NAME = "ExamPrep AI"
APP_TAGLINE = "The Student Exam Planner"
APP_ICON = "🎓"
APP_VERSION = "v2.4"
GITHUB_REPO_URL = "https://github.com/Sakshideshmukh123/AI-Smart-Study-Assistant"

# Color Palette (MyStudyLife inspired clean EdTech theme)
COLORS = {
    "primary": "#0284C7",        # Sky blue
    "primary_dark": "#0369A1",
    "primary_light": "#E0F2FE",
    "accent": "#38BDF8",
    "background": "#FAFCFE",
    "card_bg": "#FFFFFF",
    "border": "#E2E8F0",
    "text_dark": "#0F172A",
    "text_muted": "#64748B",
    "text_body": "#334155",
    "success": "#059669",
    "warning": "#D97706",
    "danger": "#DC2626",
}

# CSS Stylesheet
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #FAFCFE !important;
    color: #1E293B;
}

/* Hide default streamlit decorations */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top Header Navigation Bar ── */
.app-header-bar {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 0.75rem 1.6rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
}

.brand-text {
    font-size: 1.55rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.7px;
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.brand-text span {
    color: #0284C7;
}
.brand-icon-sq {
    background: linear-gradient(135deg, #0284C7, #38BDF8);
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.25rem;
    box-shadow: 0 4px 10px rgba(2, 132, 199, 0.28);
}

.header-tag-pill {
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    color: #0369A1;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-left: 0.4rem;
}

/* ── Top Menu Segmented Control ── */
[data-testid="stSegmentedControl"], [data-testid="stPills"] {
    background-color: transparent !important;
    justify-content: center !important;
}

[data-testid="stSegmentedControl"] button, [data-testid="stPills"] button {
    border-radius: 9999px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.45rem 1.2rem !important;
    border: 1px solid transparent !important;
    background-color: transparent !important;
    color: #475569 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSegmentedControl"] button:hover, [data-testid="stPills"] button:hover {
    color: #0284C7 !important;
    background-color: #F0F9FF !important;
}

[data-testid="stSegmentedControl"] button[aria-selected="true"], [data-testid="stPills"] button[aria-selected="true"] {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3) !important;
}

/* ── Hero Section ── */
.hero-container {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 28px;
    padding: 3.8rem 3.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px -10px rgba(2, 132, 199, 0.07);
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.16) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    color: #0284C7;
    font-size: 0.86rem;
    font-weight: 700;
    padding: 0.42rem 1.15rem;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.4rem;
    letter-spacing: 0.2px;
}
.hero-main-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.12;
    letter-spacing: -1.2px;
    margin-bottom: 1.4rem;
    max-width: 820px;
}
.hero-main-title span {
    color: #0284C7;
}
.hero-main-desc {
    font-size: 1.16rem;
    color: #475569;
    line-height: 1.65;
    max-width: 720px;
    margin-bottom: 0;
}

/* ── Card Styling ── */
.card-saas {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.03);
    transition: all 0.2s ease;
}
.card-saas:hover {
    border-color: #BAE6FD;
    transform: translateY(-2px);
    box-shadow: 0 10px 30px -4px rgba(2, 132, 199, 0.08);
}
.card-saas-title {
    font-size: 1.22rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.card-saas-desc {
    font-size: 0.95rem;
    color: #64748B;
    line-height: 1.55;
}

/* ── Metrics ── */
.metric-box-clean {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}
.metric-big-num {
    font-size: 2.5rem;
    font-weight: 800;
    color: #0284C7;
    line-height: 1;
}
.metric-sub-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.45rem;
}

/* ── Buttons ── */
.stButton > button {
    background: #0284C7 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.6rem !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #0369A1 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35) !important;
}

.stDownloadButton > button {
    background: #059669 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.6rem !important;
    box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25) !important;
}
.stDownloadButton > button:hover {
    background: #047857 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(5, 150, 105, 0.35) !important;
}

/* ── Question Card Row ── */
.question-item-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    border-left: 5px solid #0284C7;
    transition: all 0.15s ease;
}
.question-item-card:hover {
    border-color: #BAE6FD;
    box-shadow: 0 4px 18px rgba(2, 132, 199, 0.06);
}

.badge-priority {
    display: inline-block;
    padding: 0.28rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-high   { background: #FEE2E2; color: #991B1B; }
.badge-medium { background: #FEF3C7; color: #92400E; }
.badge-low    { background: #E0F2FE; color: #0369A1; }

/* ── Answer Display ── */
.model-answer-view {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #0284C7;
    border-radius: 16px;
    padding: 2.2rem;
    margin-top: 1.5rem;
    box-shadow: 0 4px 25px -2px rgba(0, 0, 0, 0.04);
    line-height: 1.75;
    color: #1E293B;
}

/* ── Notice Banners ── */
.notice-info {
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    border-radius: 14px;
    padding: 1rem 1.3rem;
    color: #0369A1;
    font-size: 0.92rem;
    font-weight: 500;
    margin-bottom: 1.2rem;
}
.notice-success {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 14px;
    padding: 1rem 1.3rem;
    color: #15803D;
    font-size: 0.92rem;
    font-weight: 500;
    margin-bottom: 1.2rem;
}

/* ── Professional SaaS Footer ── */
.app-footer-wrapper {
    background: #FFFFFF;
    border-top: 1px solid #E2E8F0;
    border-radius: 24px 24px 0 0;
    padding: 3rem 2.5rem 1.5rem 2.5rem;
    margin-top: 4rem;
    box-shadow: 0 -4px 20px -2px rgba(15, 23, 42, 0.02);
}

.footer-col-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: #0F172A;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 1rem;
}

.footer-link-item {
    font-size: 0.9rem;
    color: #64748B;
    margin-bottom: 0.55rem;
    line-height: 1.5;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.footer-link-item a {
    color: #475569;
    text-decoration: none;
    transition: color 0.2s ease;
}
.footer-link-item a:hover {
    color: #0284C7;
    text-decoration: underline;
}

.footer-tech-tag {
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    color: #475569;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    display: inline-block;
    margin: 0.2rem 0.2rem 0.2rem 0;
}

.footer-bottom-bar {
    border-top: 1px solid #F1F5F9;
    padding-top: 1.5rem;
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.8rem;
    font-size: 0.85rem;
    color: #94A3B8;
}
</style>
"""
