"""
Visual study schedule graphic generator using Matplotlib.
"""

import io
from typing import Optional

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def generate_schedule_image(schedule: list, exam_date_str: str = "") -> Optional[bytes]:
    """
    Builds a high-resolution PNG timetable card from the schedule dict.
    
    Args:
        schedule (list): List of daily plan dicts: [{"day": 1, "date": "...", "subject": "...", "hours": 3, "focus": "..."}]
        exam_date_str (str): Target examination date formatted string.
        
    Returns:
        Optional[bytes]: PNG image bytes or None if unavailable.
    """
    if not MATPLOTLIB_AVAILABLE or not schedule:
        return None

    # Modern color palette
    palette = ["#0284C7", "#0D9488", "#6366F1", "#F59E0B", "#EC4899", "#8B5CF6"]
    unique_subjs = list(dict.fromkeys(item.get("subject", "Module") for item in schedule))
    color_map = {subj: palette[i % len(palette)] for i, subj in enumerate(unique_subjs)}

    n = len(schedule)
    fig_h = max(7.5, n * 0.48 + 2.8)

    fig, ax = plt.subplots(figsize=(15, fig_h))
    fig.patch.set_facecolor("#FFFFFF")
    ax.axis("off")

    headers = ["Day", "Date", "Subject", "Hours", "Focus Topics / Objectives"]
    widths = [0.06, 0.12, 0.20, 0.08, 0.54]

    rows = []
    for s in schedule:
        rows.append([
            f"Day {s.get('day', '')}",
            str(s.get('date', '')),
            str(s.get('subject', '')),
            f"{s.get('hours', 3)} hrs",
            str(s.get('focus', ''))[:70]
        ])

    table = ax.table(
        cellText=rows,
        colLabels=headers,
        colWidths=widths,
        loc="upper center",
        cellLoc="left"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 1.8)

    # Header styling
    for j in range(len(headers)):
        c = table[(0, j)]
        c.set_facecolor("#0284C7")
        c.set_text_props(color="white", fontweight="bold")
        c.set_edgecolor("#0284C7")

    # Cell styling
    for i, s in enumerate(schedule):
        subj = s.get("subject", "Module")
        brand_hex = color_map.get(subj, "#0284C7")
        bg = "#FFFFFF" if i % 2 == 0 else "#F8FAFC"

        for j in range(len(headers)):
            cell = table[(i + 1, j)]
            cell.set_edgecolor("#E2E8F0")
            cell.set_linewidth(0.5)

            if j == 2:  # Subject column
                cell.set_facecolor("#F0F9FF")
                cell.set_text_props(color=brand_hex, fontweight="bold")
            elif j == 0:  # Day column
                cell.set_facecolor(bg)
                cell.set_text_props(color="#0F172A", fontweight="bold")
            else:
                cell.set_facecolor(bg)
                cell.set_text_props(color="#334155")

    # Title & Metadata
    fig.text(0.5, 0.985, "ExamPrep AI — Student Revision Timetable",
             ha="center", va="top", fontsize=15, fontweight="bold", color="#0F172A")
    if exam_date_str:
        fig.text(0.5, 0.958, f"Target Examination: {exam_date_str}",
                 ha="center", va="top", fontsize=10, color="#64748B")

    # Legend
    patches = [mpatches.Patch(color=color_map[s], label=s) for s in unique_subjs]
    ax.legend(handles=patches, loc="lower center", bbox_to_anchor=(0.5, -0.02),
              ncol=min(len(unique_subjs), 4), frameon=False, fontsize=9.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.94])

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
