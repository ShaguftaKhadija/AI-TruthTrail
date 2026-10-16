from pathlib import Path

import pytesseract
from PIL import Image, ImageOps, ImageFilter


# Tesseract executable ka location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    Supports common image formats such as PNG and JPG.
    """

    if not image_path:
        raise ValueError("Please provide an image path.")

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if not path.is_file():
        raise ValueError("The provided path is not a file.")

    try:
        with Image.open(path) as image:
            # Convert image into a format suitable for OCR
            image = ImageOps.exif_transpose(image)
            image = image.convert("RGB")

            # Convert to grayscale and improve contrast
            processed_image = ImageOps.grayscale(image)
            processed_image = ImageOps.autocontrast(processed_image)
            processed_image = processed_image.filter(
                ImageFilter.SHARPEN
            )

            # Extract English text
            extracted_text = pytesseract.image_to_string(
                processed_image,
                lang="eng"
            )

        extracted_text = extracted_text.strip()

        return {
            "success": True,
            "text": extracted_text,
            "character_count": len(extracted_text),
            "word_count": len(extracted_text.split()),
            "message": (
                "Text extracted successfully."
                if extracted_text
                else "No readable text was found in the image."
            )
        }

    except pytesseract.TesseractNotFoundError as error:
        raise RuntimeError(
            "Tesseract OCR was not found. Please check its installation path."
        ) from error

    except Exception as error:
        raise RuntimeError(
            f"Could not process the image: {error}"
        ) from error


if __name__ == "__main__":
    print("=" * 45)
    print("       AI TruthTrail - OCR Test")
    print("=" * 45)

    image_path = input(
        "\nEnter the complete path of your image: "
    ).strip().strip('"')

    try:
        result = extract_text_from_image(image_path)

        print("\n========== OCR RESULT ==========")
        print("Status:", result["message"])
        print("\nExtracted Text:")
        print(result["text"])
        print("\nCharacter Count:", result["character_count"])
        print("Word Count:", result["word_count"])

    except (ValueError, FileNotFoundError, RuntimeError) as error:
        print("\nError:", error)