
from pathlib import Path

from fastapi import FastAPI

from app.services.document_checker import check_claim_documents

app = FastAPI(
    title="ClaimPilot AI",
    description="Educational AI-assisted insurance claims management prototype.",
    version="0.2.0",
)


@app.get("/")
def home():
    return {
        "project": "ClaimPilot AI",
        "message": "Insurance claims assistant is running.",
        "supported_claim_categories": 12,
        "mode": "educational_prototype",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/claims/document-checks")
def get_document_checks():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "synthetic" / "claims.csv"

    results = check_claim_documents(str(csv_path))

    return {
        "total_claims": len(results),
        "claims": results,
    }


