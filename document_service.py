from io import BytesIO
import os, re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF
from utils.text_utils import sanitize_text, terms_to_list

def _lines(text):
    return [x.strip() for x in sanitize_text(text).splitlines()]

def format_txt(text):
    return sanitize_text(text).encode("utf-8")

def format_docx(text, doc_type, terms="", logo_path=None):
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(.7); section.bottom_margin = Inches(.7); section.left_margin = Inches(.8); section.right_margin = Inches(.8)
    document.styles["Normal"].font.name = "Times New Roman"
    document.styles["Normal"].font.size = Pt(11)
    if logo_path and os.path.exists(logo_path):
        p = document.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(logo_path, width=Inches(1.15))
    p = document.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"DRAFT - {doc_type.upper()}"); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(15)
    for line in _lines(text):
        if not line: document.add_paragraph(""); continue
        if line.isupper() or re.match(r"^\d+[.)]\s+", line) or line.endswith(":"):
            p = document.add_paragraph(); r = p.add_run(line); r.bold = True
        else:
            p = document.add_paragraph(line); p.paragraph_format.space_after = Pt(6)
    term_list = terms_to_list(terms)
    if term_list:
        p = document.add_paragraph(); p.add_run("TERM SUMMARY").bold = True
        table = document.add_table(rows=1, cols=2); table.style = "Table Grid"
        table.rows[0].cells[0].text = "No."; table.rows[0].cells[1].text = "Term"
        for i, term in enumerate(term_list, 1):
            cells = table.add_row().cells; cells[0].text = str(i); cells[1].text = term
    footer = section.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER; footer.add_run("Generated with LegalEase - Draft document")
    output = BytesIO(); document.save(output); return output.getvalue()

class LegalEasePDF(FPDF):
    def footer(self):
        self.set_y(-15); self.set_font("Helvetica", size=8); self.cell(0, 10, "Generated with LegalEase - Draft document", align="C")

def format_pdf(text, doc_type, logo_path=None):
    pdf = LegalEasePDF(); pdf.set_auto_page_break(auto=True, margin=18); pdf.add_page()
    if logo_path and os.path.exists(logo_path):
        try: pdf.image(logo_path, x=92, y=12, w=26); pdf.ln(28)
        except Exception: pdf.ln(4)
    else: pdf.ln(4)
    pdf.set_font("Helvetica", "B", 15); pdf.multi_cell(0, 9, f"DRAFT - {doc_type.upper()}", align="C"); pdf.ln(4)
    for line in _lines(text):
        if not line: pdf.ln(3); continue
        heading = line.isupper() or re.match(r"^\d+[.)]\s+", line) or line.endswith(":")
        pdf.set_font("Helvetica", "B" if heading else "", 10.5)
        safe = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 6, safe); pdf.ln(1)
    return bytes(pdf.output())
