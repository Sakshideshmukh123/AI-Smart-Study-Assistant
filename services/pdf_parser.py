"""
PDF extraction utility for syllabus, question papers, and faculty notes.
"""

from pypdf import PdfReader


def extract_pdf_pages(file_obj) -> tuple[str, int]:
    """
    Extracts text and page count from an uploaded PDF file.
    
    Args:
        file_obj: Streamlit UploadedFile or file-like object.
        
    Returns:
        tuple[str, int]: (combined_text, total_page_count)
    """
    reader = PdfReader(file_obj)
    full_text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        full_text += f"\n--- Page {i + 1} ---\n" + page_text

    return full_text, len(reader.pages)
