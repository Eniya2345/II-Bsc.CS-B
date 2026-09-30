from docx import Document
import io
from services.document_service import format_docx, format_pdf, format_txt
from utils.text_utils import sanitize_text
SAMPLE = """DRAFT - NDA

PARTIES
Alice (Disclosing Party), Bob (Receiving Party)

TERMS
1. Confidentiality
2. No disclosure to third parties
"""

def test_sanitize_text(): assert sanitize_text("Hello\u2019s \u2014 test") == "Hello's - test"
def test_txt(): assert b"DRAFT - NDA" in format_txt(SAMPLE)
def test_docx():
    data = format_docx(SAMPLE, "NDA", terms="Confidentiality;No disclosure")
    assert data[:2] == b"PK"
    doc = Document(io.BytesIO(data)); assert "DRAFT - NDA" in "\n".join(p.text for p in doc.paragraphs)
def test_pdf(): assert format_pdf(SAMPLE, "NDA").startswith(b"%PDF")
