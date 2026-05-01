import json
import os
from functools import wraps
import pymupdf
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

# protect the endpoint so only our server can make requests
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-Api-Key")
        if api_key != API_KEY:
            print("Invalid API Key")
            return jsonify({'error': "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated



@app.route("/health", methods=["GET"])
def health():
    return {"health": "ok"}

@app.route("/api/redact", methods=["POST"])
@require_api_key
def redact():
    search_terms = json.loads(request.form["search_terms"])
    file = request.files["file"]
    filetype = file.content_type.split("/")[-1]  # e.g. "application/pdf" → "pdf"
    doc = pymupdf.Document(stream=file.read(), filetype=filetype)
    print(f"Pages: {len(doc)}")
    print(f"Metadata: {doc.metadata}")

    for page in doc:
        for term in search_terms:
            areas = page.search_for(term)
            for rect in areas:
                page.add_redact_annot(rect, fill=(0,0,0))
        page.apply_redactions()


    return doc.tobytes(), 200, {"Content-Type": file.content_type}
