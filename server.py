import pymupdf
from flask import Flask, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return {"health": "ok"}

@app.route("/api/redact", methods=["POST"])
def redact():
    search_terms = ["Faculty", "Con vivo", "roger zare"]
    file = request.data
    filetype = request.content_type.split("/")[-1]  # e.g. "application/pdf" → "pdf"
    doc = pymupdf.Document(stream=file, filetype=filetype)
    print(f"Pages: {len(doc)}")
    print(f"Metadata: {doc.metadata}")

    for page in doc:
        for term in search_terms:
            areas = page.search_for(term)
            for rect in areas:
                page.add_redact_annot(rect, fill=(0,0,0))
        page.apply_redactions()


    return doc.tobytes(), 200, {"Content-Type": request.content_type}
