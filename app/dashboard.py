from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "data" / "synthetic" / "claims.csv"
API = "http://127.0.0.1:8010"

st.set_page_config(
    page_title="ClaimPilot AI",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background: #eef5f0;
    color: #173c2c;
}
[data-testid="stHeader"] {
    background: #eef5f0;
}
[data-testid="stSidebar"] {
    background: #d9eadf;
}
[data-testid="stSidebar"] * {
    color: #173c2c !important;
}
h1, h2, h3, p, label {
    color: #173c2c;
}
.block-container {
    padding-top: 2rem;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #c8dfcf;
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
    border-radius: 8px;
    border: none;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)


def get_api(path):
    try:
        response = requests.get(f"{API}{path}", timeout=3)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def load_claims():
    data, error = get_api("/claims")
    if isinstance(data, list):
        return pd.DataFrame(data), True, error

    if CSV_FILE.exists():
        try:
            return pd.read_csv(CSV_FILE), False, error
        except Exception as exc:
            return pd.DataFrame(), False, str(exc)

    return pd.DataFrame(), False, error


st.sidebar.title("🟢 ClaimPilot AI")
st.sidebar.caption("Insurance Claims Intelligence")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "View Claims", "Submit Claim", "AI Review", "Document Checks"],
)

st.sidebar.divider()
st.sidebar.caption("Capstone prototype")
st.sidebar.caption("Synthetic data only • Human review required")

claims, connected, connection_error = load_claims()

st.title("ClaimPilot AI")
st.subheader("Intelligent insurance claims workflow")
st.write(
    "A central workspace to review claims, check documentation, "
    "and support human-led decisions."
)

if connected:
    st.success("Backend connected. Live claims data loaded.")
else:
    st.warning(
        "Backend is not connected. Sample data may be shown; "
        "live submissions and AI reviews require FastAPI."
    )
    if connection_error:
        with st.expander("Connection details"):
            st.code(connection_error)

if page == "Dashboard":
    st.header("Operations overview")

    total = len(claims)
    if "status" in claims.columns:
        status = claims["status"].astype(str).str.lower()
        pending = int(status.isin(["new", "pending", "under review"]).sum())
        approved = int((status == "approved").sum())
        denied = int((status == "denied").sum())
    else:
        pending, approved, denied = 0, 0, 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total claims", total)
    c2.metric("Pending / review", pending)
    c3.metric("Approved", approved)
    c4.metric("Denied", denied)

    st.header("Recent claims")
    if not claims.empty:
        st.dataframe(claims.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("No claims are available. Check the dataset or start the backend.")

    st.header("How ClaimPilot works")
    a, b, c = st.columns(3)
    a.markdown("### 1. Receive")
    a.write("Capture claim details.")
    b.markdown("### 2. Validate")
    b.write("Identify missing documents.")
    c.markdown("### 3. Review")
    c.write("Provide preliminary insights for a human reviewer.")

elif page == "View Claims":
    st.header("Claims register")

    if claims.empty:
        st.info("No claims found.")
    else:
        if "claim_type" in claims.columns:
            options = ["All"] + sorted(
                claims["claim_type"].dropna().astype(str).unique().tolist()
            )
            selected = st.selectbox("Filter by claim category", options)
            shown = claims if selected == "All" else claims[
                claims["claim_type"].astype(str) == selected
            ]
        else:
            shown = claims

        st.dataframe(shown, use_container_width=True, hide_index=True)
        st.caption(f"{len(shown)} claim(s) displayed.")

    with st.form("find_claim"):
        claim_id = st.text_input("Find claim by ID", placeholder="CLM001")
        find = st.form_submit_button("Find claim")

    if find:
        result, error = get_api(f"/claims/{claim_id.strip()}")
        if result is not None:
            st.json(result)
        else:
            st.error("Could not retrieve the claim from the API.")
            if error:
                st.caption(error)

elif page == "Submit Claim":
    st.header("Submit a claim")
    st.info("Use fictional information only.")

    categories = [
        "Health/Medical", "Dental", "Disability", "Life Insurance",
        "Critical Illness", "Travel", "Mortgage Protection", "AD&D",
        "HCSA", "Dependent", "COB", "Other/Optional",
    ]

    with st.form("submit_claim"):
        claim_id = st.text_input("Claim ID", placeholder="CLM013")
        claim_type = st.selectbox("Claim category", categories)
        description = st.text_area("Claim description")
        amount = st.number_input("Claim amount (CAD)", min_value=0.0, value=100.0)
        submit = st.form_submit_button("Submit claim")

    if submit:
        if not claim_id.strip() or not description.strip():
            st.error("Enter a claim ID and description.")
        elif not connected:
            st.error("Start the FastAPI backend before submitting claims.")
        else:
            try:
                response = requests.post(
                    f"{API}/claims",
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
                else:
                    st.error(f"Submission failed: HTTP {response.status_code}")
                    st.code(response.text)
            except requests.RequestException as exc:
                st.error("Backend request failed.")
                st.code(str(exc))

elif page == "AI Review":
    st.header("AI-assisted claim review")
    st.warning(
        "This is preliminary assistance only. It does not decide coverage, "
        "eligibility, or payment."
    )

    default_id = ""
    if not claims.empty and "claim_id" in claims.columns:
        ids = claims["claim_id"].dropna().astype(str).tolist()
        if ids:
            default_id = ids[0]

    claim_id = st.text_input("Claim ID to review", value=default_id)

    if st.button("Run AI review"):
        if not claim_id.strip():
            st.error("Enter a claim ID.")
        elif not connected:
            st.error("Start the FastAPI backend before requesting a review.")
        else:
            result, error = get_api(
                f"/claims/{claim_id.strip()}/ai-review"
            )
            if result is not None:
                st.subheader("Review results")
                st.json(result)
            else:
                st.error("The review could not be completed.")
                if error:
                    st.caption(error)

elif page == "Document Checks":
    st.header("Required-document checks")
    result, error = get_api("/claims/document-checks")

    if result is not None:
        if isinstance(result, list):
            st.dataframe(
                pd.DataFrame(result),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.json(result)
    elif not claims.empty:
        st.warning("Showing the local sample claims instead.")
        st.dataframe(claims, use_container_width=True, hide_index=True)
        if error:
            st.caption(error)
    else:
        st.error("Document checks are unavailable.")
        if error:
            st.caption(error)

st.divider()
st.caption(
    "ClaimPilot AI • Educational capstone • Synthetic data only • "
    "Human oversight required"
)
