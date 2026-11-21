"""
A4 PDF report generator using ReportLab for model answers and study timetables.
"""

import io
import re
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors as rl_colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def _get_base_styles():
    brand_blue = rl_colors.HexColor("#0284C7")
    slate_dark = rl_colors.HexColor("#0F172A")
    slate_muted = rl_colors.HexColor("#64748B")

    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("HdrTitle", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=18, textColor=brand_blue, leading=22),
        "subtitle": ParagraphStyle("HdrSub", parent=ss["Normal"], fontName="Helvetica", fontSize=9, textColor=slate_muted, leading=12),
        "question": ParagraphStyle("Question", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=11, textColor=slate_dark, leading=16),
        "section": ParagraphStyle("SecTitle", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, textColor=brand_blue, spaceBefore=14, spaceAfter=6),
        "body": ParagraphStyle("AnsBody", parent=ss["Normal"], fontName="Helvetica", fontSize=10, textColor=slate_dark, leading=15, spaceAfter=4),
        "bullet": ParagraphStyle("Bullet", parent=ss["Normal"], fontName="Helvetica", fontSize=10, textColor=slate_dark, leading=15, leftIndent=15, firstLineIndent=-10, spaceAfter=3),
    }


def generate_answer_pdf(question: str, answer: str, marks: str, subject: str = "") -> bytes:
    """
    Creates a professional A4 model answer PDF.
    """
    if not REPORTLAB_AVAILABLE:
        return b""

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm
    )

    brand_blue = rl_colors.HexColor("#0284C7")
    card_bg = rl_colors.HexColor("#F8FAFC")
    border_c = rl_colors.HexColor("#E2E8F0")

    styles = _get_base_styles()
    story = []

    # Header Bar
    hdr_data = [
        [
            Paragraph("<b>🎓 ExamPrep AI</b>", styles["title"]),
            Paragraph(f"<b>{marks.upper()} MODEL ANSWER</b><br/>{datetime.now().strftime('%d %B %Y')}", styles["subtitle"])
        ]
    ]
    t = Table(hdr_data, colWidths=[11 * cm, 6 * cm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(HRFlowable(width="100%", thickness=1.5, color=brand_blue, spaceAfter=12))

    if subject:
        story.append(Paragraph(f"<b>Subject / Module:</b> {subject}", styles["subtitle"]))
        story.append(Spacer(1, 0.2 * cm))

    # Question Box
    story.append(Paragraph("EXAMINATION QUESTION", styles["section"]))
    q_box = Table([[Paragraph(question, styles["question"])]], colWidths=[17 * cm])
    q_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, brand_blue),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(q_box)
    story.append(Spacer(1, 0.4 * cm))

    # Answer Content
    story.append(Paragraph("STRUCTURED MODEL ANSWER", styles["section"]))
    for line in answer.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.15 * cm))
            continue
        if line.startswith("## ") or line.startswith("### "):
            header_text = line.lstrip("#").strip()
            story.append(Paragraph(f"<b>{header_text}</b>", styles["section"]))
        elif line.startswith("- ") or line.startswith("• "):
            text = line[2:].strip()
            clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
            story.append(Paragraph(f"• {clean}", styles["bullet"]))
        else:
            clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            story.append(Paragraph(clean, styles["body"]))

    story.append(Spacer(1, 0.8 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_c, spaceAfter=6))
    story.append(Paragraph("Prepared with ExamPrep AI · University Revision System", styles["subtitle"]))

    doc.build(story)
    return buf.getvalue()


def generate_plan_pdf(plan_text: str, subjects: list, exam_date, days_left: int) -> bytes:
    """
    Creates an A4 study timetable PDF.
    """
    if not REPORTLAB_AVAILABLE:
        return b""

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm
    )

    brand_blue = rl_colors.HexColor("#0284C7")
    border_c = rl_colors.HexColor("#E2E8F0")

    styles = _get_base_styles()
    story = []

    date_str = exam_date.strftime('%d %B %Y') if hasattr(exam_date, 'strftime') else str(exam_date)
    story.append(Paragraph("<b>ExamPrep AI — Master Study Timetable</b>", styles["title"]))
    story.append(Paragraph(f"Target Exam Date: {date_str} &nbsp;|&nbsp; Days Remaining: {days_left} Days", styles["subtitle"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=brand_blue, spaceAfter=10))

    subj_str = ", ".join(subjects) if subjects else "All Modules"
    story.append(Paragraph(f"<b>Target Subjects:</b> {subj_str}", styles["body"]))
    story.append(Spacer(1, 0.3 * cm))

    for line in plan_text.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1 * cm))
            continue
        if line.startswith("#"):
            story.append(Paragraph(f"<b>{line.lstrip('#').strip()}</b>", styles["section"]))
        else:
            clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            story.append(Paragraph(clean, styles["body"]))

    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_c, spaceAfter=6))
    story.append(Paragraph("Generated by ExamPrep AI · Smart Student Timetable", styles["subtitle"]))

    doc.build(story)
    return buf.getvalue()
