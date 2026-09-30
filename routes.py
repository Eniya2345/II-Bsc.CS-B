from pathlib import Path
from fastapi import APIRouter, HTTPException
from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest, DocumentResponse
from services.document_service import format_txt

router = APIRouter()
generator = GeminiDocumentGenerator()

@router.post("/generate", response_model=DocumentResponse)
def generate_document(payload: DocumentRequest):
    try:
        result = generator.generate_document(payload.document_type, payload.parties, payload.terms, payload.effective_date)
        return DocumentResponse(document=result.text, document_type=payload.document_type, mode=result.mode)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@router.post("/export/txt")
def export_txt(payload: DocumentRequest):
    try:
        result = generator.generate_document(payload.document_type, payload.parties, payload.terms, payload.effective_date)
        return {"filename": "legalease_document.txt", "content": format_txt(result.text).decode("utf-8")}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
