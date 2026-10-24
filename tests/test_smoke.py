import app.main as main
from fastapi.testclient import TestClient

client = TestClient(main.app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["project"] == "ClaimPilot AI"
    assert response.json()["supported_claim_categories"] == 12


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_claims_endpoint():
    response = client.get("/claims")
    assert response.status_code == 200
    assert isinstance(response.json()["claims"], list)
    assert len(response.json()["claims"]) >= 12


def test_document_checks_endpoint():
    response = client.get("/claims/document-checks")
    assert response.status_code == 200
    data = response.json()
    assert "total_claims" in data
    assert "claims" in data


def test_ai_review_existing_claim():
    response = client.get("/claims/CLM001/ai-review")
    assert response.status_code == 200
    assert "decision" in response.json()


def test_missing_claim_returns_404():
    response = client.get("/claims/CLAIM-DOES-NOT-EXIST")
    assert response.status_code == 404


def test_ai_review_missing_claim_returns_404():
    response = client.get("/claims/CLAIM-DOES-NOT-EXIST/ai-review")
    assert response.status_code == 404


def test_negative_amount_is_rejected():
    response = client.post(
        "/claims",
        json={
            "claim_id": "TEST-NEGATIVE",
            "claim_type": "Dental",
            "description": "Validation test",
            "amount": -100,
        },
    )
    assert response.status_code == 422


def test_unsupported_category_is_rejected():
    response = client.post(
        "/claims",
        json={
            "claim_id": "TEST-INVALID-CATEGORY",
            "claim_type": "Unknown",
            "description": "Validation test",
            "amount": 100,
        },
    )
    assert response.status_code == 422


def test_duplicate_claim_id_is_rejected(monkeypatch):
    monkeypatch.setattr(
        main,
        "load_claims",
        lambda: [{"claim_id": "TEST-DUPLICATE"}],
    )

    response = client.post(
        "/claims",
        json={
            "claim_id": "TEST-DUPLICATE",
            "claim_type": "Dental",
            "description": "Duplicate test",
            "amount": 100,
        },
    )
    assert response.status_code == 409


def test_valid_claim_submission_does_not_write_real_storage(monkeypatch):
    saved = []

    monkeypatch.setattr(main, "load_claims", lambda: [])
    monkeypatch.setattr(main, "save_claim", lambda claim: saved.append(claim))

    response = client.post(
        "/claims",
        json={
            "claim_id": "TEST-SAFE-SUBMISSION",
            "claim_type": "Dental",
            "description": "Automated test claim",
            "amount": 125,
        },
    )

    assert response.status_code == 201
    assert response.json()["claim"]["claim_id"] == "TEST-SAFE-SUBMISSION"
    assert len(saved) == 1
