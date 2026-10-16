import json
from pathlib import Path
from datetime import datetime, timezone


HISTORY_FILE = Path(__file__).with_name("claim_history.json")


def load_history():
    """Load saved claim history from the JSON file."""

    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            raise ValueError(
                "Claim history file must contain a list."
            )

        # Validate the structure of each saved record.
        for item in history:
            if not isinstance(item, dict):
                raise ValueError(
                    "Invalid record found in claim history."
                )

            if not isinstance(item.get("claim_id"), str):
                raise ValueError(
                    "A saved record has an invalid claim ID."
                )

            if (
                not isinstance(item.get("version"), int)
                or isinstance(item.get("version"), bool)
                or item["version"] < 1
            ):
                raise ValueError(
                    "A saved record has an invalid version number."
                )

        return history

    except json.JSONDecodeError as error:
        raise ValueError(
            "Claim history file contains invalid JSON."
        ) from error


def save_history(history):
    """Save claim history to the JSON file."""

    if not isinstance(history, list):
        raise ValueError("History must be a list.")

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_claim_version(claim_id, claim_text, source="", notes=""):
    """Add a new version of a claim."""

    # Validate inputs.
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise ValueError("Please provide a claim ID.")

    if not isinstance(claim_text, str) or not claim_text.strip():
        raise ValueError("Please provide the claim text.")

    if not isinstance(source, str):
        raise ValueError("Source must be text.")

    if not isinstance(notes, str):
        raise ValueError("Notes must be text.")

    claim_id = claim_id.strip()
    claim_text = claim_text.strip()
    source = source.strip()
    notes = notes.strip()

    # Load existing history.
    history = load_history()

    # Find the highest existing version for this claim.
    existing_versions = [
        item["version"]
        for item in history
        if item.get("claim_id") == claim_id
    ]

    version_number = max(existing_versions, default=0) + 1

    # Create a new record.
    record = {
        "claim_id": claim_id,
        "version": version_number,
        "claim_text": claim_text,
        "source": source,
        "notes": notes,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    # Save the new record.
    history.append(record)
    save_history(history)

    return record


def get_claim_history(claim_id):
    """Retrieve all saved versions of a claim."""

    if not isinstance(claim_id, str) or not claim_id.strip():
        raise ValueError("Please provide a claim ID.")

    claim_id = claim_id.strip()
    history = load_history()

    return [
        item
        for item in history
        if item.get("claim_id") == claim_id
    ]


if __name__ == "__main__":

    print("=" * 45)
    print("   AI TruthTrail - Claim History Test")
    print("=" * 45)

    claim_id = input("\nEnter a claim ID: ").strip()
    claim_text = input("Enter the claim text: ").strip()
    source = input("Enter the source name (optional): ").strip()
    notes = input("Enter notes (optional): ").strip()

    try:
        record = add_claim_version(
            claim_id=claim_id,
            claim_text=claim_text,
            source=source,
            notes=notes
        )

        print("\n===== Saved Claim Version =====")
        print(
            json.dumps(
                record,
                indent=4,
                ensure_ascii=False
            )
        )

        print("\n===== Complete Claim History =====")

        versions = get_claim_history(claim_id)

        for version in versions:
            print(f"\nVersion: {version['version']}")
            print(f"Claim: {version['claim_text']}")
            print(f"Source: {version['source']}")
            print(f"Notes: {version['notes']}")
            print(f"Recorded at: {version['recorded_at']}")

        print("\nClaim history saved successfully!")

    except (ValueError, OSError) as error:
        print("\nError:", error)