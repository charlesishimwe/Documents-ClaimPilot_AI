# ClaimPilot AI — Intelligent Insurance Claims Workflow

**An AI-assisted insurance claims management prototype built with FastAPI, Streamlit, Python, and automated testing.**

[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-176B45)](https://claimpilot-ai-dashboard.onrender.com/)
[![API Health](https://img.shields.io/badge/API-Health%20Check-success)](https://documents-claimpilot-ai.onrender.com/health)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/charlesishimwe/Documents-ClaimPilot_AI/actions)

## 1. Project Overview

ClaimPilot AI is an educational prototype designed to support insurance claims workflows. It helps organize claims, identify missing documentation, validate claim submissions, and generate preliminary AI-assisted assessments for human review.

The project demonstrates how a Python API, a web dashboard, structured synthetic data, automated tests, and cloud deployment can work together in an insurance technology application.

**Important:** ClaimPilot AI is a prototype, not a production insurance platform. It does not make binding coverage or payment decisions. All preliminary assessments require human review.

## 2. Project Objectives

- Organize insurance claims and their associated information.
- Support 12 insurance claim categories.
- Check required documentation and identify missing documents.
- Validate claim submissions, including claim amounts and supported categories.
- Provide preliminary claim assessments and suggested next steps.
- Offer a web dashboard for viewing, submitting, and reviewing claims.
- Demonstrate automated testing, continuous integration, and cloud deployment.

## 3. Live Application

| Component | Link |
|---|---|
| ClaimPilot AI Dashboard | https://claimpilot-ai-dashboard.onrender.com/ |
| FastAPI Backend | https://documents-claimpilot-ai.onrender.com/ |
| API Health Check | https://documents-claimpilot-ai.onrender.com/health |
| Interactive API Documentation | https://documents-claimpilot-ai.onrender.com/docs |
| GitHub Repository | https://github.com/charlesishimwe/Documents-ClaimPilot_AI |
| GitHub Actions | https://github.com/charlesishimwe/Documents-ClaimPilot_AI/actions |

The dashboard connects to the deployed FastAPI backend using the `CLAIMPILOT_API_URL` environment variable.

## 4. Supported Insurance Claim Categories

ClaimPilot AI includes the following 12 categories:

1. Health/Medical
2. Dental
3. Disability
4. Life Insurance
5. Critical Illness
6. Travel
7. Mortgage Protection
8. Accidental Death and Dismemberment (AD&D)
9. Health Care Spending Account (HCSA)
10. Dependent
11. Coordination of Benefits (COB)
12. Other/Optional

The project uses synthetic sample claims for demonstration and testing.

## 5. Main Features

### Claims Management
- View sample claims and their statuses.
- Submit claims through the dashboard.
- Validate supported claim categories and claim amounts.
- Retrieve claims through the API.

### Document Verification
- Compare received documents against required documents.
- Identify missing documents.
- Suggest next steps to help complete claim files.

### AI-Assisted Preliminary Review
- Summarize claim information.
- Identify documentation gaps.
- Provide preliminary assessments and suggested next steps.
- Require human review rather than making binding insurance decisions.

**Implementation note:** The current assessment component is primarily rule-based. It should not be described as a fully autonomous or production-grade large language model agent.

### Interactive Dashboard
The Streamlit dashboard provides:
- Operations overview
- Claims listing
- Claim submission
- AI-assisted review
- Document checks

### Quality and Deployment
- FastAPI backend
- Automated tests with pytest
- GitHub Actions continuous integration
- Render deployment for the API and dashboard

## 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| FastAPI | REST API |
| Streamlit | Interactive web dashboard |
| Pandas | Claims data processing |
| Requests | Dashboard-to-API communication |
| JSON and CSV | Synthetic data and prototype persistence |
| Pytest | Automated testing |
| HTTPX | API testing dependency |
| Git and GitHub | Version control and collaboration |
| GitHub Actions | Continuous integration |
| Render | Cloud deployment |

## 7. System Architecture

```text
                  User
                   |
                   v
          Streamlit Dashboard
                   |
                   | HTTP requests
                   v
             FastAPI Backend
                   |
        +----------+-----------+
        |          |           |
        v          v           v
    Claims      Document     Preliminary
    Workflow     Checker     AI Review
        |          |           |
        +----------+-----------+
                   |
                   v
         Synthetic Claims Data
          CSV / JSON Storage
```

The dashboard communicates with the API over HTTP. The backend exposes endpoints for health checks, claims retrieval, document checks, claim submission, and preliminary review.

## 8. Project Structure

```text
Documents:ClaimPilot_AI/
├── app/
│   ├── main.py
│   ├── dashboard.py
│   └── services/
│       ├── claims_workflow.py
│       ├── claims_ai_agent.py
│       ├── document_checker.py
│       └── claim_storage.py
├── data/
│   ├── synthetic/
│   │   └── claims.csv
│   └── storage/
├── docs/
│   ├── PROJECT_SCOPE.md
│   ├── DESIGN_AND_TESTING.md
│   └── AGILE_SPRINT_BOARD.md
├── tests/
│   └── test_smoke.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```

## 9. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Project information |
| GET | `/health` | Backend health check |
| GET | `/docs` | Interactive Swagger API documentation |
| GET | `/claims` | Retrieve claims |
| GET | `/claims/document-checks` | Check required documentation |
| GET | `/claims/{claim_id}/ai-review` | Generate a preliminary review |
| POST | `/claims` | Submit a claim |

The deployed Swagger documentation at `/docs` can be used to inspect available endpoints and their request and response schemas.

## 10. Local Installation

### Prerequisites

- Python 3.11 recommended
- Git
- A terminal
- A web browser

### Clone the repository

```bash
git clone https://github.com/charlesishimwe/Documents-ClaimPilot_AI.git
cd Documents-ClaimPilot_AI
```

### Create and activate a virtual environment

On macOS or Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Start the FastAPI backend

In the project directory, run:

```bash
uvicorn app.main:app --reload --port 8010
```

Open the interactive API documentation:

http://127.0.0.1:8010/docs

### Start the Streamlit dashboard

Open a second terminal, activate the same virtual environment, and navigate to the project directory.

Set the API URL:

```bash
export CLAIMPILOT_API_URL=http://127.0.0.1:8010
```

Start the dashboard:

```bash
streamlit run app/dashboard.py
```

Streamlit will display the local dashboard URL in the terminal.

## 11. Running Automated Tests

Run the test suite from the project root:

```bash
python -m pytest -v
```

The current local test run completed with **11 passed**.

The tests cover core API behavior, health checks, claims retrieval, document checks, preliminary review, missing claims, validation, duplicate claim IDs, and safe submission behavior.

The GitHub Actions workflow runs automated tests when configured repository events occur. Check the Actions tab for the latest execution results.

## 12. Continuous Integration and Deployment

The project uses GitHub Actions for automated testing and Render for hosting.

The CI workflow:
1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies.
4. Runs the pytest suite.

Render hosts the FastAPI backend and Streamlit dashboard separately. The dashboard uses `CLAIMPILOT_API_URL` to locate the backend.

Deployment and CI status should be verified in the live services and GitHub Actions before a release or academic submission.

## 13. Security, Privacy, and Responsible AI

- The project is designed to use synthetic demonstration data.
- Do not upload real customer records or sensitive insurance information.
- Validate submitted claim data before processing.
- Treat preliminary assessments as decision support, not final decisions.
- Require qualified human review for insurance decisions.
- Do not interpret missing documents as proof that a claim is invalid.
- Protect deployment configuration and avoid committing secrets or API keys.
- JSON file storage is intended for demonstration, not concurrent production workloads.

## 14. Limitations and Future Improvements

### Current Limitations
- Preliminary assessments are primarily rule-based.
- The prototype does not connect to a real insurer's claims administration system.
- JSON storage does not provide production-grade transactional persistence.
- The system does not establish policy coverage or determine binding payment eligibility.
- Synthetic sample claims do not represent real customer outcomes.

### Potential Improvements
- Integrate a controlled LLM-based agent with grounded retrieval and citations.
- Add a production database and database migrations.
- Introduce authentication, role-based authorization, and audit logging.
- Improve document ingestion and extraction.
- Add broader integration and end-to-end dashboard tests.
- Implement monitoring, tracing, and secure secrets management.
- Evaluate assessment quality using a documented test dataset.

## 15. Agile Development

The project is organized into three sprints:

- **Sprint 1 — Foundation and Claims Data:** Application structure, API, synthetic dataset, and document checker.
- **Sprint 2 — Workflow, AI Review, and Dashboard:** Claims workflow, persistence, preliminary review, and user interface.
- **Sprint 3 — Quality, Deployment, and Submission:** Automated testing, CI/CD, cloud deployment, documentation, and demonstration.

See [`docs/AGILE_SPRINT_BOARD.md`](docs/AGILE_SPRINT_BOARD.md) for the task board and [`docs/DESIGN_AND_TESTING.md`](docs/DESIGN_AND_TESTING.md) for architecture and testing details.

## 16. Academic Project Information

**Project:** ClaimPilot AI — Intelligent Insurance Claims Workflow  
**Presenter:** Charles Ishimwe  
**Program:** Quantic School of Business and Technology — Software Engineering / AI Engineering capstone

This project demonstrates practical software engineering, API development, workflow automation, preliminary AI-assisted analysis, testing, continuous integration, and cloud deployment.

## 17. References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Documentation](https://render.com/docs)

---

**Disclaimer:** ClaimPilot AI is an educational prototype. It is not intended to provide insurance, legal, financial, or medical advice, nor to make real insurance coverage or payment decisions.
