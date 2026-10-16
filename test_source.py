from source_engine import analyze_source


print("===== AI TruthTrail Source Engine Test =====")

source_name = input("\nEnter source name: ")
url = input("Enter source URL (optional): ")
publication_date = input(
    "Enter publication date (YYYY-MM-DD, optional): "
)
notes = input("Enter additional notes (optional): ")

try:
    result = analyze_source(
        source_name=source_name,
        url=url,
        publication_date=publication_date,
        notes=notes
    )

    print("\n===== Test Result =====")

    for key, value in result.items():
        print(f"{key}: {value}")

except ValueError as error:
    print("\nTest Error:", error)