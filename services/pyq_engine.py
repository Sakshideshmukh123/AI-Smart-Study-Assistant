"""
Question extraction, normalization, and repetition frequency analysis engine.
"""

import re
from collections import defaultdict


def parse_questions_from_text(text: str) -> list[str]:
    """
    Scans raw text from exam papers and extracts candidate question lines.
    
    Args:
        text (str): Extracted PDF content.
        
    Returns:
        list[str]: Clean list of extracted exam questions.
    """
    lines = text.split("\n")
    p_num = re.compile(r"^(?:Q\.?\s*)?(\d+)[.)]\s+(.+)", re.IGNORECASE)
    p_sub = re.compile(r"^\(?([a-z]|i{1,3}|iv|v)\)\s+(.+)", re.IGNORECASE)
    p_end = re.compile(r".+\?\s*$")
    p_verbs = re.compile(
        r"\b(explain|define|describe|discuss|differentiate|compare|write|list|state|"
        r"what is|what are|how does|why is|derive|prove|calculate|find|determine|"
        r"analyze|evaluate|illustrate)\b",
        re.IGNORECASE
    )

    questions = []
    current_q = ""

    for line in lines:
        s = line.strip()
        if len(s) < 10 or s.startswith("--- Page") or re.match(r"^(Time|Max|Note|Section|PART)", s, re.IGNORECASE):
            continue

        is_question = bool(
            p_num.match(s) or p_sub.match(s) or p_end.match(s) or p_verbs.search(s)
        )

        if is_question:
            if current_q and len(current_q) > 15:
                questions.append(current_q.strip())
            current_q = s
        elif current_q:
            current_q += " " + s

    if current_q and len(current_q) > 15:
        questions.append(current_q.strip())

    return questions


def normalize_question(question: str) -> str:
    """
    Normalizes question string to enable matching across different years and formats.
    """
    q = question.lower()
    q = re.sub(r"^(q\.?\s*)?\d+[.)]\s*", "", q)
    q = re.sub(r"^\(?[a-z]\)\s*", "", q)
    q = re.sub(r"[^\w\s]", "", q)
    return re.sub(r"\s+", " ", q).strip()


def run_pyq_analysis(pyq_docs: dict) -> list[dict]:
    """
    Analyzes uploaded PYQ papers to identify repeated questions.

    Args:
        pyq_docs (dict): {paper_name: {"text": str, "pages": int}}

    Returns:
        list[dict]: Sorted list of questions ranked by frequency.
    """
    norm_map = defaultdict(list)
    total_papers = len(pyq_docs)

    for paper_name, data in pyq_docs.items():
        seen = set()
        for q in parse_questions_from_text(data["text"]):
            norm = normalize_question(q)
            if norm and len(norm) > 10 and norm not in seen:
                norm_map[norm].append((q, paper_name))
                seen.add(norm)

    results = []
    for norm, occurrences in norm_map.items():
        appeared_in = list({p for _, p in occurrences})
        best_original = max((q for q, _ in occurrences), key=len)
        results.append({
            "question": best_original,
            "normalized": norm,
            "frequency": len(appeared_in),
            "total": total_papers,
            "appeared_in": appeared_in
        })

    # Sort descending: highest frequency first
    results.sort(key=lambda x: x["frequency"], reverse=True)
    return results
