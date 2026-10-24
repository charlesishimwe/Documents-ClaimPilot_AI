cat > app/services/claims_ai_agent.py <<'PY'
def analyze_claim(claim):
    """Provide a preliminary educational review of a fictional claim."""

    description = str(
        claim.get("claim_description")
        or claim.get("description")
        or ""
    )

    amount_value = claim.get("claim_amount")
    if amount_value is None:
        amount_value = claim.get("amount", 0)

    try:
        amount = float(amount_value)
    except (TypeError, ValueError):
        amount = 0.0

    required = str(claim.get("required_documents") or "")
    received = str(claim.get("documents_received") or "")

    required_docs = {
        item.strip().lower(): item.strip()
        for item in required.split(";")
        if item.strip()
    }

    received_docs = {
        item.strip().lower()
        for item in received.split(";")
        if item.strip()
    }

    missing_docs = [
        original_name
        for key, original_name in required_docs.items()
        if key not in received_docs
    ]

    if missing_docs:
        summary = (
            "Some documents appear to be missing. "
            "Verify the document checklist."
        )
        next_steps = [
            f"Verify or request: {doc}" for doc in missing_docs
        ]
    else:
        summary = (
            "No missing documents were identified by this basic "
            "checklist. Further review may still be required."
        )
        next_steps = [
            "Verify the claim details and applicable policy terms.",
            "Refer the claim to an authorized human reviewer.",
        ]

    return {
        "claim_id": claim.get("claim_id", "Unknown"),
        "claim_type": claim.get("claim_type", "Unknown"),
        "amount": amount,
        "description_summary": description[:300],
        "missing_documents": missing_docs,
        "preliminary_assessment": summary,
        "suggested_next_steps": next_steps,
        "decision": "Human review required",
        "disclaimer": (
            "Educational prototype only. This assessment does not "
            "determine insurance coverage or payment."
        ),
    }
PY