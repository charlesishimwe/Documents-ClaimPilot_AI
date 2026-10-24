
import csv


def check_claim_documents(csv_path):
    results = []

    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for claim in reader:
            received = {
                item.strip().lower()
                for item in claim["documents_received"].split(";")
                if item.strip()
            }

            required = {
                item.strip().lower()
                for item in claim["required_documents"].split(";")
                if item.strip()
            }

            missing = sorted(required - received)

            results.append({
                "claim_id": claim["claim_id"],
                "claim_type": claim["claim_type"],
                "missing_documents": missing,
                "complete": len(missing) == 0,
            })

    return results


if __name__ == "__main__":
    claims = check_claim_documents("data/synthetic/claims.csv")

    for claim in claims:
        print(f"\nClaim: {claim['claim_id']} - {claim['claim_type']}")

        if claim["complete"]:
            print("Document check: Complete")
        else:
            print("Missing documents:", ", ".join(claim["missing_documents"]))
