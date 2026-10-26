# ClaimPilot AI — Agile Sprint Board

## Project Goal
Build and deploy an educational AI-assisted insurance claims prototype that checks documents, organizes claims, and provides preliminary assessments for human review.

## Sprint 1 — Foundation and Claims Data
**Sprint goal:** Establish the application foundation and prepare synthetic claims data.

| Task | Expected outcome | Status |
|---|---|---|
| Create project structure | Organized application and documentation folders | Completed |
| Configure FastAPI | API starts and exposes health endpoints | Completed |
| Create synthetic claims dataset | Sample claims covering 12 categories | Completed |
| Implement document checker | Identify missing required documents | Completed |
| Add automated tests | Verify core API and validation behavior | Completed |

## Sprint 2 — Workflow, AI Review, and Dashboard
**Sprint goal:** Implement the claims workflow and provide a usable dashboard.

| Task | Expected outcome | Status |
|---|---|---|
| Implement claims workflow | Create and find claims; validate amounts | Completed |
| Build preliminary AI review | Summarize claims and identify missing documents | Completed |
| Add claim persistence | Save submitted claims to JSON storage | Completed |
| Build Streamlit dashboard | Dashboard, claims list, submission, AI review, and document checks | Completed |
| Validate dashboard-to-API connection | Confirm live dashboard data and submissions work | Needs verification |
| Add input validation and safeguards | Reject invalid claim types and negative amounts | Completed |

## Sprint 3 — Quality, Deployment, and Submission
**Sprint goal:** Test, deploy, document, and prepare the capstone demonstration.

| Task | Expected outcome | Status |
|---|---|---|
| Create automated test suite | Tests cover core API and claim behavior | Completed |
| Configure GitHub Actions CI | Run automated tests on repository changes | Configured; verify latest run |
| Deploy FastAPI backend | Public API and documentation are accessible | Completed; verify availability before submission |
| Deploy Streamlit dashboard | Public web interface is accessible | Completed; verify live API connection |
| Write design and testing document | Document architecture, testing, security, and limitations | Draft created; review against final implementation |
| Prepare project README | Installation, features, endpoints, and deployment instructions | Needs verification |
| Confirm repository access | Ensure the Quantic grader has the required access | Needs verification |
| Record final demonstration | 15–20 minute screen/voiceover video in MP4 or MOV | Pending |
| Share demonstration | Google Drive link accessible to anyone with the link | Pending |
| Final submission review | Check documentation, test results, deployment, and citations | Pending |

## Definition of Done
A task is considered complete only when its result has been implemented and verified. Deployment status, automated test results, repository permissions, and the public dashboard/API connection must be checked before final submission.

## Known Limitations
- This is an educational prototype using synthetic claims data.
- AI assessments are preliminary and must not replace qualified human review.
- The prototype does not make binding insurance coverage or payment decisions.
- JSON file persistence is suitable for a small demonstration, not a production claims platform.
