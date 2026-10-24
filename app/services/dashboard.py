
import pandas as pd
import streamlit as st
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "synthetic" / "claims.csv"
API_URL = "http://127.0.0.1:8010"

st.set_page_config(
    page_title="ClaimPilot AI",
    page_icon="🟢",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f8f5;
    color: #193b2b;
}
[data-testid="stSidebar"] {
    background-color: #e2eee6;
}
h1, h2, h3, p, label {
    color: #193b2b;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border: 1px solid #d4e3d8;
    border-radius: 12px;
}
[data-testid="stMetricValue"] {
    color: #176b45;
}
.stButton > button, .stFormSubmitButton > button {
    background: #176b45;
    color: white;
    border-radius: 8px;
    min-height: 40px;
}
</style>
""", unsafe_allow_html=True)


def get_api(path):
    try:
        response = requests.get(f"{API_URL}{path}", timeout=3)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def get_claims():
    data, error = get_api("/claims")
    if isinstance(data, list):
        return pd.DataFrame(data), True, None

    if CSV_PATH.exists():
        try:
            return pd.read_csv(CSV_PATH), False, error
        except Exception as exc:
            return pd.DataFrame(), False, str(exc)

    return pd.DataFrame(), False, error


st.sidebar.title("🟢 ClaimPilot AI")
st.sidebar.caption("Insurance Claims Intelligence")
page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "View Claims", "Submit Claim", "AI Review", "Document Checks"],
)

claims, connected, error = get_claims()

st.title("ClaimPilot AI")
st.subheader("Intelligent Insurance Claims Workflow")
st.write(
    "Review claims, identify missing documentation, "
    "and support human-led insurance workflows."
)

if connected:
    st.success("FastAPI backend connected.")
else:
    st.warning("Showing sample data if available. Live operations require the API.")
    if error:
        st.caption(f"Backend status: {error}")

if page == "Dashboard":
    st.header("Operations Overview")

    total = len(claims)
    if "status" in claims.columns:
        statuses = claims["status"].astype(str).str.lower()
        pending = int(statuses.isin(["new", "pending", "under review"]).sum())
        approved = int((statuses == "approved").sum())
        denied = int((statuses == "denied").sum())
    else:
        pending, approved, denied = 0, 0, 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Claims", total)
    c2.metric("Pending / Review", pending)
    c3.metric("Approved", approved)
    c4.metric("Denied", denied)

    st.header("Recent Claims")
    if not claims.empty:
        st.dataframe(claims.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("No sample claims found. Check the dataset.")

    st.header("Workflow")
    a, b, c = st.columns(3)
    a.markdown("### 1. Receive")
    a.write("Capture claim details.")
    b.markdown("### 2. Validate")
    b.write("Check supporting documents.")
    c.markdown("### 3. Review")
    c.write("Assist authorized human reviewers.")

elif page == "View Claims":
    st.header("Claims Register")
    if claims.empty:
        st.info("No claims are available.")
    else:
        st.dataframe(claims, use_container_width=True, hide_index=True)

    claim_id = st.text_input("Find a claim by ID")
    if st.button("Find Claim"):
        if not claim_id.strip():
            st.error("Enter a claim ID.")
        else:
            result, detail = get_api(f"/claims/{claim_id.strip()}")
            if result is not None:
                st.json(result)
            else:
                st.error("Could not retrieve the claim.")
                st.caption(detail or "Check the backend.")

elif page == "Submit Claim":
    st.header("Submit a New Claim")
    st.info("Use fictional data only.")

    categories = [
        "Health/Medical", "Dental", "Disability", "Life Insurance",
        "Critical Illness", "Travel", "Mortgage Protection", "AD&D",
        "HCSA", "Dependent", "COB", "Other/Optional",
    ]

    with st.form("new_claim"):
        claim_id = st.text_input("Claim ID")
        claim_type = st.selectbox("Claim Category", categories)
        description = st.text_area("Claim Description")
        amount = st.number_input("Claim Amount (CAD)", min_value=0.0, value=100.0)
        submit = st.form_submit_button("Submit Claim")

    if submit:
        if not claim_id.strip() or not description.strip():
            st.error("Claim ID and description are required.")
        elif not connected:
            st.error("Start the FastAPI backend before submitting.")
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
                    st.success("Claim submitted.")
                    st.json(response.json())
                else:
                    st.error(f"Submission failed: HTTP {response.status_code}")
                    st.code(response.text)
            except requests.RequestException as exc:
                st.error(str(exc))

elif page == "AI Review":
    st.header("AI-Assisted Claim Review")
    st.warning(
        "This is preliminary assistance only. It does not decide coverage or payment."
    )
    claim_id = st.text_input("Claim ID to review")
    if st.button("Run AI Review"):
        if not claim_id.strip():
            st.error("Enter a claim ID.")
        elif not connected:
            st.error("Start the FastAPI backend first.")
        else:
            result, detail = get_api(
                f"/claims/{claim_id.strip()}/ai-review"
            )
            if result is not None:
                st.json(result)
            else:
                st.error("Review failed.")
                st.caption(detail or "Check the backend.")

elif page == "Document Checks":
    st.header("Required Document Checks")
    result, detail = get_api("/claims/document-checks")
    if result is not None:
        if isinstance(result, list):
            st.dataframe(pd.DataFrame(result), use_container_width=True)
        else:
            st.json(result)
    elif not claims.empty:
        st.warning("Showing local sample data instead.")
        st.dataframe(claims, use_container_width=True, hide_index=True)
        st.caption(detail or "")
    else:
        st.error("Document checks are unavailable.")
        st.caption(detail or "")

st.divider()
st.caption(
    "ClaimPilot AI | Educational prototype | Synthetic data only | "
    "Human review required for real-world decisions"
)
