from urllib.parse import urlparse
from datetime import date as date_type


def analyze_source(source_name, url="", publication_date="", notes=""):
    """
    Organize and validate basic source information.

    This module checks the format of a URL and publication date.
    It does not independently verify the source's authenticity,
    credibility, or factual accuracy.
    """

    # Clean and validate input types
    source_name = (
        source_name.strip()
        if isinstance(source_name, str)
        else ""
    )

    url = url.strip() if isinstance(url, str) else ""

    publication_date = (
        publication_date.strip()
        if isinstance(publication_date, str)
        else ""
    )

    notes = notes.strip() if isinstance(notes, str) else ""

    # Source name is required
    if not source_name:
        raise ValueError("Please provide the source name.")

    # Validate URL format if provided
    url_status = "not_provided"

    if url:
        parsed_url = urlparse(url)

        if (
            parsed_url.scheme not in ("http", "https")
            or not parsed_url.hostname
            or "." not in parsed_url.hostname
            or any(char.isspace() for char in url)
        ):
            raise ValueError(
                "Please provide a valid HTTP or HTTPS URL."
            )

        url_status = "format_valid_not_verified"

    # Validate publication date if provided
    date_status = "not_provided"

    if publication_date:
        try:
            date_type.fromisoformat(publication_date)
        except ValueError:
            raise ValueError(
                "Please enter the publication date "
                "in YYYY-MM-DD format."
            )

        date_status = "format_valid_not_verified"

    # Identify missing information
    missing_information = []

    if not url:
        missing_information.append("source URL")

    if not publication_date:
        missing_information.append("publication date")

    if not notes:
        missing_information.append("additional notes")

    # Prepare result
    return {
        "source_name": source_name,
        "url": url,
        "publication_date": publication_date,
        "notes": notes,
        "url_status": url_status,
        "date_status": date_status,
        "missing_information": missing_information,
        "verification_status": "not_independently_verified",
        "message": (
            "Source information has been organized. "
            "The source's authenticity and credibility "
            "have not been independently verified."
        )
    }


if __name__ == "__main__":

    print("===== AI TruthTrail Source Analysis Test =====")

    source_name = input(
        "\nEnter the source or website name: "
    )

    url = input(
        "Enter the source URL (optional): "
    )

    publication_date = input(
        "Enter publication date (YYYY-MM-DD, optional): "
    )

    notes = input(
        "Enter additional notes (optional): "
    )

    try:
        result = analyze_source(
            source_name=source_name,
            url=url,
            publication_date=publication_date,
            notes=notes
        )

        print("\n===== Source Analysis Result =====")

        for key, value in result.items():
            print(f"{key}: {value}")

    except ValueError as error:
        print("\nInput Error:", error)