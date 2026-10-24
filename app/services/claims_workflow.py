CLAIM_STATUSES = [
    "New",
    "Pending",
    "Under Review",
    "Approved",
    "Denied",
]


def create_claim(claim_id, claim_type, description, amount):
    if amount < 0:
        raise ValueError("Claim amount cannot be negative.")

    return {
        "claim_id": claim_id,
        "claim_type": claim_type,
        "description": description,
        "amount": amount,
        "currency": "CAD",
        "status": "New",
    }


def find_claim(claims, claim_id):
    for claim in claims:
        if claim["claim_id"] == claim_id:
            return claim
    return None
