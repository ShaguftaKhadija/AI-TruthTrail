from deep_translator import GoogleTranslator

print("Testing translation...")

try:
    translator = GoogleTranslator(
        source="en",
        target="hi"
    )

    result = translator.translate(
        "Climate change may increase global temperatures."
    )

    print("\nTranslation successful!")
    print("Result:", result)

except Exception as error:
    print("\nTranslation failed!")
    print("Actual error:", repr(error))