# from urllib.parse import urlparse


# def analyze_evidence(claim, source, quote, url="", date="", notes=""):
#     """
#     Validate and organize evidence submitted for a claim.

#     This function checks whether the required fields are present
#     and whether the supplied URL has a valid basic structure.
#     It does not independently verify the source or prove the claim.
#     """

#     claim = claim.strip() if isinstance(claim, str) else ""
#     source = source.strip() if isinstance(source, str) else ""
#     quote = quote.strip() if isinstance(quote, str) else ""
#     url = url.strip() if isinstance(url, str) else ""
#     date = date.strip() if isinstance(date, str) else ""
#     notes = notes.strip() if isinstance(notes, str) else ""

#     if not claim:
#         raise ValueError("Please provide a claim.")

#     if not source:
#         raise ValueError("Please provide the source name.")

#     if not quote:
#         raise ValueError("Please provide a supporting quote.")

#     url_status = "not_provided"

#     if url:
#         parsed_url = urlparse(url)

#         if (
#             parsed_url.scheme not in ("http", "https")
#             or not parsed_url.netloc
#             or "." not in parsed_url.netloc
#         ):
#             raise ValueError(
#                 "Please provide a valid HTTP or HTTPS source URL."
#             )

#         url_status = "format_valid_not_verified"

#     return {
#         "claim": claim,
#         "source": source,
#         "quote": quote,
#         "url": url,
#         "date": date,
#         "notes": notes,
#         "url_status": url_status,
#         "evidence_status": "submitted_not_independently_verified",
#         "message": (
#             "Evidence details have been organized. "
#             "The source and quote have not been independently verified."
#         )
#     }

# from urllib.parse import urlparse
# from datetime import date as date_type


# def analyze_evidence(
#     claim,
#     source,
#     quote,
#     url="",
#     date="",
#     notes=""
# ):
#     """
#     Validate and organize evidence submitted for a claim.

#     This function validates input fields and organizes evidence.
#     It does not independently verify the source, quote, or claim.
#     """

#     # Validate and clean text inputs
#     claim = claim.strip() if isinstance(claim, str) else ""
#     source = source.strip() if isinstance(source, str) else ""
#     quote = quote.strip() if isinstance(quote, str) else ""
#     url = url.strip() if isinstance(url, str) else ""
#     date = date.strip() if isinstance(date, str) else ""
#     notes = notes.strip() if isinstance(notes, str) else ""

#     # Required field validation
#     if not claim:
#         raise ValueError("Please provide a claim.")

#     if not source:
#         raise ValueError("Please provide the source name.")

#     if not quote:
#         raise ValueError("Please provide a supporting quote.")

#     # URL validation
#     url_status = "not_provided"

#     if url:
#         parsed_url = urlparse(url)

#         if (
#             parsed_url.scheme not in ("http", "https")
#             or not parsed_url.hostname
#             or "." not in parsed_url.hostname
#             or any(char.isspace() for char in url)
#         ):
#             raise ValueError(
#                 "Please provide a valid HTTP or HTTPS source URL."
#             )

#         url_status = "format_valid_not_verified"

#     # Optional date validation: YYYY-MM-DD
#     date_status = "not_provided"

#     if date:
#         try:
#             date_type.fromisoformat(date)
#         except ValueError:
#             raise ValueError(
#                 "Please enter the date in YYYY-MM-DD format."
#             )

#         date_status = "format_valid_not_verified"

#     # Identify missing optional information
#     missing_information = []

#     if not url:
#         missing_information.append("source URL")

#     if not date:
#         missing_information.append("publication date")

#     if not notes:
#         missing_information.append("additional notes")

#     # Organize the evidence record
#     return {
#         "claim": claim,
#         "source": source,
#         "quote": quote,
#         "url": url,
#         "date": date,
#         "notes": notes,

#         "url_status": url_status,
#         "date_status": date_status,

#         "missing_information": missing_information,

#         "evidence_status": "submitted_not_independently_verified",

#         "message": (
#             "Evidence details have been organized. "
#             "The source, quote, and claim have not been "
#             "independently verified."
#         )
#     }

from urllib.parse import urlparse
from datetime import date as date_type


def is_valid_url(url):
    """
    Validate the basic structure of an HTTP or HTTPS URL.
    This does not verify whether the website actually exists.
    """
    if not isinstance(url, str) or not url.strip():
        return False

    url = url.strip()

    try:
        parsed_url = urlparse(url)

        return (
            parsed_url.scheme.lower() in ("http", "https")
            and bool(parsed_url.hostname)
            and "." in parsed_url.hostname
            and not any(char.isspace() for char in url)
        )
    except (ValueError, AttributeError):
        return False


def analyze_evidence(
    claim,
    source,
    quote,
    url="",
    date="",
    notes=""
):
    """
    Validate and organize evidence submitted for a claim.

    This function checks required fields, URL format, and date format.
    It does not independently verify the source, quote, or claim.
    """

    # Clean input fields
    claim = claim.strip() if isinstance(claim, str) else ""
    source = source.strip() if isinstance(source, str) else ""
    quote = quote.strip() if isinstance(quote, str) else ""
    url = url.strip() if isinstance(url, str) else ""
    date = date.strip() if isinstance(date, str) else ""
    notes = notes.strip() if isinstance(notes, str) else ""

    # Validate required fields
    if not claim:
        raise ValueError("Please provide a claim.")

    if not source:
        raise ValueError("Please provide the source name.")

    if not quote:
        raise ValueError("Please provide a supporting quote.")

    # Validate source URL
    url_status = "not_provided"

    if url:
        if not is_valid_url(url):
            raise ValueError(
                "Invalid source URL. Please enter a valid HTTP or HTTPS URL, "
                "such as https://example.com/article."
            )

        url_status = "format_valid_not_verified"

    # Validate optional date
    date_status = "not_provided"

    if date:
        try:
            parsed_date = date_type.fromisoformat(date)

            # Ensure the input follows YYYY-MM-DD exactly
            if parsed_date.isoformat() != date:
                raise ValueError

        except ValueError:
            raise ValueError(
                "Invalid date. Please use YYYY-MM-DD format, "
                "for example 2026-10-14."
            )

        date_status = "format_valid_not_verified"

    # Identify missing optional information
    missing_information = []

    if not url:
        missing_information.append("source URL")

    if not date:
        missing_information.append("publication date")

    if not notes:
        missing_information.append("additional notes")

    # Return the organized record
    return {
        "claim": claim,
        "source": source,
        "quote": quote,
        "url": url,
        "date": date,
        "notes": notes,
        "url_status": url_status,
        "date_status": date_status,
        "missing_information": missing_information,
        "evidence_status": "submitted_not_independently_verified",
        "message": (
            "Evidence details have been organized. "
            "The source, quote, and claim have not been "
            "independently verified."
        )
    }