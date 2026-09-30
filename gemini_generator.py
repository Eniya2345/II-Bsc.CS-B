import os
from dataclasses import dataclass
from dotenv import load_dotenv
from utils.text_utils import sanitize_text

load_dotenv()

@dataclass
class GenerationResult:
    text: str
    mode: str

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
        self._client = None
        if self.api_key:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)

    def generate_document(self, document_type, parties, terms, effective_date):
        if not self._client:
            return GenerationResult(self._demo_document(document_type, parties, terms, effective_date), "demo")
        prompt = self._build_prompt(document_type, parties, terms, effective_date)
        try:
            response = self._client.models.generate_content(model=self.model_name, contents=prompt)
            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return GenerationResult(sanitize_text(text), "gemini")
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

    @staticmethod
    def _build_prompt(document_type, parties, terms, effective_date):
        formatted_terms = "\n".join(f"- {x.strip()}" for x in terms.split(";") if x.strip())
        return f"""You are LegalEase, a legal-document drafting assistant.

Create a professional DRAFT legal document based strictly on the supplied information. Do not invent names, addresses, dates, payments, governing laws, penalties, or obligations that the user did not provide. Where a legally important detail is missing, use [TO BE COMPLETED].

Document type: {document_type}
Parties: {parties}
Effective date: {effective_date}
Requested terms:\n{formatted_terms}

Requirements:
1. Use a clear formal title.
2. Include the effective date and parties.
3. Organize the document into numbered sections.
4. Convert each requested term into an appropriate clause.
5. Include signature blocks where appropriate.
6. Use plain but professional legal language.
7. Mark the result as a DRAFT.
8. Do not claim that the document is legally valid in a particular jurisdiction.
9. Do not provide a legal opinion.
10. Return only document text, without Markdown code fences.""".strip()

    @staticmethod
    def _demo_document(document_type, parties, terms, effective_date):
        clauses = "\n\n".join(f"{i}. {x.strip()}" for i, x in enumerate(terms.split(";"), 1) if x.strip()) or "1. [TO BE COMPLETED]"
        return f"""DRAFT - {document_type.upper()}

Effective Date: {effective_date}

PARTIES
{parties}

PURPOSE
This draft is prepared from the information supplied through LegalEase. It is a document-generation demonstration and should be reviewed and completed before use.

TERMS AND CONDITIONS

{clauses}

GENERAL
Any missing information should be completed by the parties. Applicable jurisdiction-specific requirements should be reviewed by a qualified professional before execution.

SIGNATURES

Party 1: ______________________________
Name: __________________________________
Date: __________________________________

Party 2: ______________________________
Name: __________________________________
Date: __________________________________"""
