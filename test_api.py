from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_root():
    r = client.get("/"); assert r.status_code == 200; assert r.json()["name"] == "LegalEase API"

def test_health():
    r = client.get("/health"); assert r.status_code == 200; assert r.json()["status"] == "ok"

def test_generate_demo(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    import backend.routes as routes
    from ai_core.gemini_generator import GeminiDocumentGenerator
    monkeypatch.setattr(routes, "generator", GeminiDocumentGenerator())
    r = client.post("/generate", json={"document_type":"NDA","parties":"Alice (Disclosing Party), Bob (Receiving Party)","terms":"Confidentiality;No disclosure to third parties","effective_date":"2026-04-15"})
    assert r.status_code == 200; assert r.json()["mode"] == "demo"; assert "NDA" in r.json()["document"]

def test_generate_validation():
    r = client.post("/generate", json={"document_type":"","parties":"Alice","terms":"Confidentiality","effective_date":"2026-04-15"})
    assert r.status_code == 422
