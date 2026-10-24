cat > app.py <<'PY'
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

# -------------------- Configuration --------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "synthetic" / "claims.csv"
API_URL = "http://127.0.0.1:8010"

st.set_page_config(
    page_title="ClaimPilot AI",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Styling --------------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f8f5;
    color: #193b2b;
}
[data-testid="stHeader"] {
    background: #f4f8f5;
}
[data-testid="stSidebar"] {
    background: #e2eee6;
}
[data-testid="stSidebar"] * {
    color: #193b2b;
}
.block-container {
    padding-top: 2rem;
    max-width: 1500px;
}
h1, h2, h3, p, label {
    color: #193b2b;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #d4e3d8;
    border-radius: 12px;
    padding: 16px;
}
div[data-testid="stMetricValue"] {
    color: #176b45;
}
.stButton > button,
.stFormSubmitButton > button {
    background: #176b45;
    color: white;
    border: none;
    border-radius: 8px;
    min-height: 42px;
    font-weight: 600;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #105335;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -------------------- Backend helpers --------------------
def api_get(path):
    try:
        response = requests.get(f"{API_URL}{path}", timeout=4)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def load_claims():
    data, error = api_get("/claims")

    if isinstance(data, list):
        return pd.DataFrame(data), True, None

    if CSV_PATH.exists():
        try:
            return pd.read_csv(CSV_PATH), False, error
        except Exception as exc:
            return pd.DataFrame(), False, str(exc)

    return pd.DataFrame(), False, error or "Claims dataset was not found."


def display_table(data):
    if isinstance(data, list):
        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True,
            hide_index=True,
        )
    elif isinstance(data, dict):
        st.json(data)
    else:
        st.info("No results are available.")


# -------------------- Sidebar --------------------
st.sidebar.markdown("# 🟢 ClaimPilot AI")
st.sidebar.caption("Insurance Claims Intelligence")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "View Claims",
        "Submit Claim",
        "AI Review",
        "Document Checks",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Capstone educational prototype")
st.sidebar.caption("Synthetic data only • Human oversight required")

claims, connected, connection_error = load_claims()

# -------------------- Main header --------------------
st.title("ClaimPilot AI")
st.subheader("Intelligent Insurance Claims Workflow")
st.write(
    "A unified workspace to review claim information, "
    "check documentation, and support human-led decisions."
)

if connected:
    st.success("Connected to the FastAPI backend.")
else:
    st.warning(
        "Backend unavailable. Local sample data is shown when available. "
        "Live submission and AI review require the backend."
    )
    if connection_error:
        with st.expander("Connection details"):
            st.code(connection_error)


# -------------------- Dashboard --------------------
if page == "Dashboard":
    st.header("Operations Overview")

    total = len(claims)
    if "status" in claims.columns:
        status = claims["status"].astype(str).str.lower()
        pending = int(status.isin(["new", "pending", "under review"]).sum())
        approved = int((status == "approved").sum())
        denied = int((status == "denied").sum())
    else:
        pending, approved, denied = 0, 0, 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Claims", total)
    c2.metric("Pending / Review", pending)
    c3.metric("Approved", approved)
    c4.metric("Denied", denied)

    st.header("Recent Claims")
    if not claims.empty:
        st.dataframe(
            claims.head(10),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No claims found. Check the sample dataset.")

    st.header("How ClaimPilot Works")
    a, b, c = st.columns(3)
    with a:
        st.markdown("### 1. Receive")
        st.write("Capture claim details.")
    with b:
        st.markdown("### 2. Validate")
        st.write("Identify missing documents.")
    with c:
        st.markdown("### 3. Review")
        st.write("Support an authorized human reviewer.")


# -------------------- View Claims --------------------
elif page == "View Claims":
    st.header("Claims Register")

    if claims.empty:
        st.info("No claims are available.")
    else:
        filtered = claims.copy()

        if "claim_type" in filtered.columns:
            options = ["All"] + sorted(
                filtered["claim_type"].dropna().astype(str).unique().tolist()
            )
            selected = st.selectbox("Filter by claim category", options)
            if selected != "All":
                filtered = filtered[
                    filtered["claim_type"].astype(str) == selected
                ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"{len(filtered)} claim(s) displayed.")

    with st.form("find_claim"):
        st.subheader("Find a Claim")
        claim_id = st.text_input("Claim ID", placeholder="CLM001")
        find_clicked = st.form_submit_button("Find Claim")

    if find_clicked:
        if not claim_id.strip():
            st.error("Enter a claim ID.")
        else:
            result, error = api_get(f"/claims/{claim_id.strip()}")
            if result is not None:
                st.json(result)
            else:
                st.error("The claim could not be retrieved from the API.")
                if error:
                    st.caption(error)


# -------------------- Submit Claim --------------------
elif page == "Submit Claim":
    st.header("Submit a New Claim")
    st.info("Use fictional information only.")

    categories = [
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

    with st.form("submit_new_claim"):
        claim_id = st.text_input("Claim ID", placeholder="CLM013")
        claim_type = st.selectbox("Claim Category", categories)
        description = st.text_area("Claim Description")
        amount = st.number_input(
            "Claim Amount (CAD)",
            min_value=0.0,
            value=100.0,
            step=25.0,
        )
        submit_clicked = st.form_submit_button("Submit Claim")

    if submit_clicked:
        if not claim_id.strip() or not description.strip():
            st.error("Claim ID and description are required.")
        elif not connected:
            st.error("Start the FastAPI backend before submitting claims.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/claims",
                    json={
                        "claim_id": claim_id.strip(),
                        "claim_type": claim_type,
                        "description": description.strip(),
                        "amount": amount,
                    },
                    timeout=10,
                )

                if response.status_code in (200, 201):
                    st.success("Claim submitted successfully.")
                    st.json(response.json())
                    st.rerun()
                else:
                    st.error(f"Submission failed: HTTP {response.status_code}")
                    st.code(response.text)
            except requests.RequestException as exc:
                st.error("Could not contact the backend.")
                st.code(str(exc))


# -------------------- AI Review --------------------
elif page == "AI Review":
    st.header("AI-Assisted Claim Review")
    st.warning(
        "Preliminary assistance only. This prototype does not decide "
        "coverage, eligibility, or payment."
    )

    default_id = ""
    if not claims.empty and "claim_id" in claims.columns:
        ids = claims["claim_id"].dropna().astype(str).tolist()
        if ids:
            default_id = ids[0]

    claim_id = st.text_input("Claim ID to review", value=default_id)

    if st.button("Run AI Review", type="primary"):
        if not claim_id.strip():
            st.error("Enter a claim ID.")
        elif not connected:
            st.error("Start the FastAPI backend before running AI review.")
        else:
            result, error = api_get(
                f"/claims/{claim_id.strip()}/ai-review"
            )
            if result is not None:
                st.subheader("Review Results")
                st.json(result)
            else:
                st.error("AI review failed.")
                if error:
                    st.caption(error)


# -------------------- Document Checks --------------------
elif page == "Document Checks":
    st.header("Required Document Checks")

    result, error = api_get("/claims/document-checks")

    if result is not None:
        display_table(result)
    elif not claims.empty:
        st.warning("Showing local sample claims because the API is unavailable.")
        st.dataframe(
            claims,
            use_container_width=True,
            hide_index=True,
        )
        if error:
            st.caption(error)
    else:
        st.error("Document checks are unavailable.")
        if error:
            st.caption(error)


# -------------------- Footer --------------------
st.divider()
st.caption(
    "ClaimPilot AI • Capstone prototype • Synthetic data only • "
    "Human review required for real-world decisions"
)
PY