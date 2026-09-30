# LegalEase — AI-Powered Legal Document Generator

Complete implementation of the supplied LegalEase specification: Streamlit frontend, FastAPI backend, Gemini integration, editable preview, TXT/DOCX/PDF exports, tests, environment configuration, and Docker support.

The source document specifies Gemini 1.5 Pro. Because model names/SDKs can change, this implementation uses the current `google-genai` SDK and makes the model configurable with `GEMINI_MODEL` (default: `gemini-2.5-flash`). Set it to any Gemini model available to your account.

> LegalEase creates draft documents for informational/document-drafting purposes. It is not a substitute for review by a qualified lawyer.

## Structure

```text
LegalEase/
├── app.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── pytest.ini
├── README.md
├── backend/{__init__.py,routes.py,schemas.py}
├── ai_core/{__init__.py,gemini_generator.py}
├── services/{__init__.py,document_service.py}
├── utils/{__init__.py,text_utils.py}
├── assets/logo.svg
├── tests/{__init__.py,test_api.py,test_document_service.py}
└── scripts/{test_api.ps1,test_api.sh}
```

## VS Code setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
BACKEND_URL=http://127.0.0.1:8000
APP_TITLE=LegalEase
MAX_DOCUMENT_CHARS=50000
```

If `GEMINI_API_KEY` is empty, LegalEase runs in demo mode, so the frontend, API, editing, and exports can still be tested.

## Run

Terminal 1:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API: `http://127.0.0.1:8000/`  
Swagger: `http://127.0.0.1:8000/docs`  
Health: `http://127.0.0.1:8000/health`

Terminal 2:

```bash
streamlit run app.py
```

Frontend: `http://localhost:8501`

## Test

```bash
pytest
```

Manual test: enter document type, parties, semicolon-separated terms, and effective date; click Generate; edit the output; download TXT, DOCX, and PDF.

Example:

```text
Document type: Freelance Work Contract
Parties: Jane Doe (Service Provider), TechNova Inc. (Client)
Terms: Payment within 30 days;Confidentiality;Deadline for delivery;Termination with 15 days notice
Effective date: April 15, 2026
```

## Docker

```bash
docker compose build
docker compose up
```

Backend: port 8000. Frontend: port 8501.

## Security / production

Never commit `.env`. For production add authentication, rate limiting, HTTPS, encrypted storage, audit logging, jurisdiction-specific templates, human/legal review, and persistent storage. Avoid sending unnecessary sensitive personal information to external AI services.
