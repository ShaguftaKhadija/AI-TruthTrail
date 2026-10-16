# from evidence_engine import analyze_evidence

# print("=" * 45)
# print("       AI TruthTrail - Evidence Trail")
# print("=" * 45)

# claim = input("\nEnter the claim: ")
# source = input("Enter the source name: ")
# quote = input("Enter the supporting quote: ")
# url = input("Enter the source URL (optional): ")
# date = input("Enter the publication date (YYYY-MM-DD, optional): ")
# notes = input("Enter additional notes (optional): ")

# try:
#     result = analyze_evidence(
#         claim=claim,
#         source=source,
#         quote=quote,
#         url=url,
#         date=date,
#         notes=notes
#     )

#     print("\n" + "=" * 45)
#     print("          EVIDENCE RECORD")
#     print("=" * 45)

#     print("\nClaim:", result["claim"])
#     print("Source:", result["source"])
#     print("Supporting Quote:", result["quote"])
#     print("URL:", result["url"] or "Not provided")
#     print("Date:", result["date"] or "Not provided")
#     print("Notes:", result["notes"] or "Not provided")

#     print("\nURL Status:", result["url_status"])
#     print("Date Status:", result["date_status"])
#     print("Evidence Status:", result["evidence_status"])

#     if result["missing_information"]:
#         print(
#             "\nMissing Information:",
#             ", ".join(result["missing_information"])
#         )
#     else:
#         print("\nNo optional information is missing.")

#     print("\nMessage:", result["message"])

# except ValueError as error:
#     print("\nInput Error:", error)

from evidence_engine import analyze_evidence

print("=" * 45)
print("       AI TruthTrail - Evidence Trail")
print("=" * 45)

claim = input("\nEnter the claim: ")
source = input("Enter the source name: ")
quote = input("Enter the supporting quote: ")
url = input("Enter the source URL (optional): ")
date = input("Enter the publication date (YYYY-MM-DD, optional): ")
notes = input("Enter additional notes (optional): ")

try:
    result = analyze_evidence(
        claim=claim,
        source=source,
        quote=quote,
        url=url,
        date=date,
        notes=notes
    )

    print("\n" + "=" * 45)
    print("          EVIDENCE RECORD")
    print("=" * 45)

    print("\nClaim:", result["claim"])
    print("Source:", result["source"])
    print("Supporting Quote:", result["quote"])
    print("URL:", result["url"] or "Not provided")
    print("Date:", result["date"] or "Not provided")
    print("Notes:", result["notes"] or "Not provided")

    print("\nURL Status:", result["url_status"])
    print("Date Status:", result["date_status"])
    print("Evidence Status:", result["evidence_status"])

    if result["missing_information"]:
        print(
            "\nMissing Information:",
            ", ".join(result["missing_information"])
        )
    else:
        print("\nNo optional information is missing.")

    print("\nMessage:", result["message"])

except ValueError as error:
    print("\nInput Error:", error)