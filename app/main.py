import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.claim_storage import save_claim, load_saved_claims
from app.services.document_checker import check_claim_documents
from app.services.claims_workflow import create_claim, find_claim
from app.services.claims_ai_agent import analyze_claim

app = FastAPI(
    title="ClaimPilot AI",
    description="Educational AI-assisted insurance claims prototype.",
    version="0.4.0",
)

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "synthetic"
    / "claims.csv"
)

SUPPORTED_CATEGORIES = [
    "Health/Medical",
    "Dental",
    "Disability",
    "Life Insurance",
    "Critical Illness",
    "Travel",
    "Mortgage Protection",
    "AD&D",
    "HCSA",
    "Dependent",
    "COB",
    "Other/Optional",
]


class NewClaim(BaseModel):
    claim_id: str = Field(min_length=1, max_length=50)
    claim_type: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=2000)
    amount: float = Field(ge=0, le=100000000)


def load_csv_claims():
    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Claims dataset is unavailable.",
        )

    with open(DATA_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_claims():
    """Return original sample claims and persisted submissions."""
    try:
        original_claims = load_csv_claims()
        saved_claims = load_saved_claims()
        return original_claims + saved_claims
    except HTTPException:
        raise
    except (OSError, ValueError, TypeError):
        raise HTTPException(
            status_code=500,
            detail="Claims data could not be loaded.",
        )


@app.get("/")
def home():
    return {
        "project": "ClaimPilot AI",
        "message": "Insurance claims assistant is running.",
        "supported_claim_categories": len(SUPPORTED_CATEGORIES),
        "mode": "educational_prototype",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/claims")
def list_claims():
    return {"claims": load_claims()}


@app.get("/claims/document-checks")
def get_document_checks():
    results = check_claim_documents(str(DATA_FILE))
    return {
        "total_claims": len(results),
        "claims": results,
    }


@app.get("/claims/{claim_id}/ai-review")
def review_claim_with_ai(claim_id: str):
    claim_id = claim_id.strip()
    claim = find_claim(load_claims(), claim_id)

    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    return analyze_claim(claim)


@app.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    claim = find_claim(load_claims(), claim_id.strip())

    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim


@app.post("/claims", status_code=201)
def submit_claim(new_claim: NewClaim):
    claim_id = new_claim.claim_id.strip()
    claim_type = new_claim.claim_type.strip()
    description = new_claim.description.strip()

    if not claim_id or not claim_type or not description:
        raise HTTPException(
            status_code=422,
            detail="Claim ID, category, and description cannot be blank.",
        )

    if claim_type not in SUPPORTED_CATEGORIES:
        raise HTTPException(
            status_code=422,
            detail="Unsupported claim category.",
        )

    claims = load_claims()

    if find_claim(claims, claim_id):
        raise HTTPException(
            status_code=409,
            detail="Claim ID already exists.",
        )

    try:
        claim = create_claim(
            claim_id,
            claim_type,
            description,
            new_claim.amount,
        )
        save_claim(claim)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except (OSError, TypeError, RuntimeError):
        raise HTTPException(
            status_code=500,
            detail="The claim could not be saved.",
        )

    return {
        "message": "Claim submitted successfully",
        "claim": claim,
    }
