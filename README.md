# OpenCare — Python Server

Flask microservice that redacts sensitive terms from uploaded files (PDFs and images) before they are stored in MinIO.

## Stack

- **Flask** — HTTP server
- **PyMuPDF** (`pymupdf`) — PDF and image manipulation

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/redact` | Redact search terms from a PDF or image file |

### `POST /api/redact`

Requires the `X-Api-Key` header matching `API_KEY`.

**Form fields:**
- `file` — the uploaded PDF or image file
- `search_terms` — JSON-encoded array of strings to redact

Returns the redacted file with its original content type.

## Run

```bash
python -m venv .venv

# Windows: .venv\Scripts\activate
source .venv/bin/activate   

# Mac/Linux: .venv\Scripts\activate
. .venv/bin/activate        

pip install flask pymupdf
python run.py               # dev server on :5000
```