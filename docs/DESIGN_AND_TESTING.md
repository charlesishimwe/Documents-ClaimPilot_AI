# ClaimPilot AI — Design and Testing Documentation

## 1. Project Overview

ClaimPilot AI is an educational prototype that demonstrates an AI-assisted
insurance claims workflow. It uses synthetic sample claims to demonstrate
claim listing, document completeness checks, claim submission, and
preliminary AI-assisted review.

The system is not an insurer's production platform. It does not make binding
coverage, payment, or denial decisions. Human review is required.

## 2. Objectives

- Support 12 insurance claim categories.
- Display sample and submitted claims.
- Validate new claim submissions.
- Identify missing required documents.
- Generate preliminary claim review summaries.
- Expose functionality through a FastAPI backend.
- Provide a browser-based Streamlit dashboard.
- Run automated tests through GitHub Actions.

## 3. Technology Stack

- Python
- FastAPI for REST API endpoints
- Pydantic for request validation
- Streamlit for the dashboard
- Pandas for tabular claim data
- CSV for synthetic sample data
- JSON file storage for submitted prototype claims
- Pytest and FastAPI TestClient for automated tests
- GitHub Actions for continuous integration
- Render for cloud hosting

## 4. Architecture

The dashboard sends HTTP requests to the FastAPI backend.

The backend exposes endpoints for health checks, listing claims,
document checks, claim submission, individual claim lookup, and preliminary
AI-assisted review.

The prototype combines synthetic CSV claims with claims saved in JSON.
The dashboard may show local sample data when the API is unavailable.
Live features require a successful connection to the backend.

## 5. Main Features

### Claim categories

Health/Medical, Dental, Disability, Life Insurance, Critical Illness,
Travel, Mortgage Protection, AD&D, HCSA, Dependent, COB, and Other/Optional.

### Claim workflow

New claims are validated for required fields, supported categories,
non-negative amounts, and duplicate claim IDs. Valid submissions receive
the initial status "New".

### Document checks

The document checker compares received documents with required documents
and identifies items that appear to be missing.

### AI-assisted review

The current review service is rule-based. It produces a preliminary summary,
identifies missing documents, and suggests next steps. It is not a
large-language-model system and does not replace human review.

## 6. API Endpoints

- GET / — application information
- GET /health — health status
- GET /claims — sample and saved claims
- GET /claims/document-checks — document completeness results
- POST /claims — submit a claim
- GET /claims/{claim_id} — retrieve a claim
- GET /claims/{claim_id}/ai-review — preliminary review

## 7. Testing Strategy

Automated tests cover:
- Home and health endpoints
- Listing claims and document checks
- Reviewing an existing claim
- Handling unknown claim IDs
- Rejecting negative claim amounts
- Rejecting unsupported claim categories
- Rejecting duplicate claim IDs
- Accepting a valid submission without writing test data to real storage

## 8. Test Execution

Run the automated tests from the project root:

    python -m pytest -v

Record the actual test result and date before submission. Do not report
tests as passing unless the command completes successfully.

## 9. Security and Privacy

- Use synthetic data only for this educational prototype.
- Do not upload real insurance claim or customer information.
- Validate claim input using Pydantic and application rules.
- Keep secrets and environment files out of version control.
- Restrict production access and add authentication before any real-world use.
- Use HTTPS for public service communication.
- Review storage durability, access controls, audit logging, and retention
  before considering production deployment.

## 10. Limitations

- The AI review is rule-based, not a trained model or LLM agent.
- JSON file storage is suitable only for a small demonstration.
- Production-grade authentication, authorization, and audit trails are not
  implemented by this prototype.
- Cloud-hosted local files may not provide durable storage across restarts
  or deployments.
- The dashboard must be verified against the live backend before claiming
  that all live features work.

## 11. Deployment and CI

The backend and dashboard are hosted as separate Render web services.
GitHub Actions runs automated tests on repository updates. The final
submission should include links to the repository, deployed dashboard,
backend health endpoint, and API documentation.

## 12. Final Acceptance Checklist

- [ ] Public dashboard opens and displays correctly.
- [ ] Dashboard successfully connects to the public backend.
- [ ] Sample claims appear on the View Claims page.
- [ ] A synthetic test claim can be submitted.
- [ ] Document checks return results.
- [ ] AI-assisted review returns a preliminary summary.
- [ ] Unknown claim IDs return an appropriate not-found response.
- [ ] GitHub Actions completes successfully.
- [ ] At least three Agile sprints are documented.
- [ ] Demo recording and submission links are ready.
