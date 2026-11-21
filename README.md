# 🎓 ExamPrep AI — Smart University Exam Preparation Platform

An intelligent, full-stack university exam assistant built with **Streamlit**, **Google Gemini AI**, **ReportLab**, and **Matplotlib**. 

Designed to streamline revision by identifying question trends across past year papers, generating marks-calibrated model answers with 1-click A4 PDF export, and creating automated visual study timetables.

---

## ✨ Features

- 📂 **Study Materials Library**: Upload and organize course documents across **Syllabus**, **PYQ Papers**, and **Faculty Notes** with live text previews.
- 🔍 **PYQ Trends Analyzer**: Pattern-matches and normalizes questions across multiple exam papers to highlight high-frequency, repeated topics with priority badges.
- ✍️ **AI Model Answer Studio**: Generates structured, professor-grade answers calibrated for **2 Marks**, **5 Marks**, or **10 Marks**. One-click export to printable **A4 PDF**.
- 📅 **Visual Study Planner**: Builds day-by-day revision timetables based on target exam dates and available study hours, exporting to:
  - 🖼️ **Visual Schedule Card (PNG)**: Clean lockscreen-friendly schedule.
  - 📄 **A4 Master Timetable (PDF)**: Printable revision roadmap.

---

## 🏗️ Project Architecture

The project follows a clean, decoupled modular structure designed for maintainability and scalability:

```
ExamPrep-AI/
├── app.py                      # Main application orchestrator & router
├── config.py                   # Global constants, theme tokens, and custom CSS
├── requirements.txt            # Project dependencies
├── services/                   # Core business logic and rendering engines
│   ├── __init__.py
│   ├── gemini_service.py       # Google Gemini SDK wrapper & model routing
│   ├── pdf_parser.py           # PDF text extraction and page counting
│   ├── pyq_engine.py           # Question parsing, regex normalization & ranking
│   ├── report_generator.py     # ReportLab A4 PDF generator (answers & plans)
│   └── visualizer.py           # Matplotlib timetable card visualizer
└── views/                      # UI view components
    ├── __init__.py
    ├── navbar.py               # Top navigation bar & API key modal
    ├── home_view.py            # Overview dashboard & metric highlights
    ├── library_view.py         # File upload dropzones & management
    ├── pyq_view.py             # PYQ repetition trends & filters
    ├── answer_view.py          # AI answer generator & PDF export
    └── planner_view.py         # Timetable generation & visual exports
```

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ExamPrep-AI.git
cd ExamPrep-AI
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key (Optional)
You can set your API key as an environment variable or enter it directly within the web app:
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your-api-key"

# Linux / macOS
export GEMINI_API_KEY="your-api-key"
```
> *Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).*

### 5. Launch the application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Large Language Model**: [Google Gemini](https://ai.google.dev/) via `google-genai` SDK
- **PDF Extraction**: [pypdf](https://pypi.org/project/pypdf/)
- **PDF Generation**: [ReportLab](https://www.reportlab.com/)
- **Visual Data Cards**: [Matplotlib](https://matplotlib.org/) & [Pillow](https://python-pillow.org/)

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
