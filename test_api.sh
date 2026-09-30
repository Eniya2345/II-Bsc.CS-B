#!/usr/bin/env bash
curl -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d '{"document_type":"NDA","parties":"Alice (Disclosing Party), Bob (Receiving Party)","terms":"Confidentiality;No disclosure to third parties","effective_date":"2026-04-15"}'
