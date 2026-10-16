import re
from deep_translator import GoogleTranslator


# ==========================================
# AI TruthTrail - Translation Engine
# ==========================================

SUPPORTED_LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "urdu": "ur",
    "bengali": "bn",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "arabic": "ar",
    "chinese": "zh-CN",
    "japanese": "ja",
    "portuguese": "pt",
    "russian": "ru"
}


UNCERTAINTY_WORDS = {
    "may", "might", "could", "possibly",
    "potentially", "suggest", "suggests",
    "suggested", "likely", "unlikely",
    "preliminary", "appears", "seems"
}


STRONG_CERTAINTY_WORDS = {
    "proves", "prove", "proven", "confirmed",
    "definitely", "certainly", "undoubtedly",
    "always", "never", "guaranteed"
}


def clean_text(text):
    """Clean and validate text."""

    if not isinstance(text, str):
        return ""

    return re.sub(r"\s+", " ", text).strip()


def get_language_code(language):
    """Convert a language name into its language code."""

    if not isinstance(language, str):
        raise ValueError("Please provide a valid language name.")

    language = language.strip().lower()

    if language not in SUPPORTED_LANGUAGES:
        available = ", ".join(SUPPORTED_LANGUAGES.keys())

        raise ValueError(
            f"Unsupported language. Available languages: {available}"
        )

    return SUPPORTED_LANGUAGES[language]


def translate_text(text, source_language, target_language):
    """
    Translate text using GoogleTranslator through deep-translator.

    Requires an internet connection.
    """

    text = clean_text(text)

    if not text:
        raise ValueError("Please enter text to translate.")

    source_code = get_language_code(source_language)
    target_code = get_language_code(target_language)

    if source_code == target_code:
        return {
            "original_text": text,
            "translated_text": text,
            "source_language": source_language.lower(),
            "target_language": target_language.lower(),
            "status": "same_language"
        }

    try:
        # translator = GoogleTranslator(
        #     source=source_code,
        #     target=target_code
        # )

        # translated_text = translator.translate(text)

        if not translated_text:
            raise ValueError("The translation service returned no text.")

        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_language.lower(),
            "target_language": target_language.lower(),
            "status": "translated"
        }

    except ValueError:
        raise

    except Exception as error:
        raise RuntimeError(
            "Translation failed. Check your internet connection "
            "and try again."
        ) from error


def find_certainty_words(text):
    """Find English certainty-related words in text."""

    words = set(re.findall(r"\b[a-z]+\b", text.lower()))

    return {
        "uncertainty_words": sorted(words & UNCERTAINTY_WORDS),
        "strong_certainty_words": sorted(
            words & STRONG_CERTAINTY_WORDS
        )
    }


def analyze_translation_drift(original_text, translated_text):
    """
    Identify possible wording differences between two text versions.

    This is a basic English keyword-based check, not a full
    semantic translation-quality evaluation.
    """

    original_text = clean_text(original_text)
    translated_text = clean_text(translated_text)

    if not original_text or not translated_text:
        raise ValueError(
            "Both original and translated text are required."
        )

    original_markers = find_certainty_words(original_text)
    translated_markers = find_certainty_words(translated_text)

    findings = []

    missing_uncertainty = sorted(
        set(original_markers["uncertainty_words"])
        - set(translated_markers["uncertainty_words"])
    )

    added_strong_certainty = sorted(
        set(translated_markers["strong_certainty_words"])
        - set(original_markers["strong_certainty_words"])
    )

    if missing_uncertainty:
        findings.append({
            "type": "Possible Uncertainty Wording Change",
            "details": missing_uncertainty,
            "description": (
                "Uncertainty-related words found in the original "
                "are not present in the translated text. "
                "Review the meaning in context."
            )
        })

    if added_strong_certainty:
        findings.append({
            "type": "Possible Stronger Certainty",
            "details": added_strong_certainty,
            "description": (
                "Strong certainty-related words appear in the "
                "translated text but not in the original."
            )
        })

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "findings": findings,
        "finding_count": len(findings),
        "status": (
            "possible_drift_detected"
            if findings
            else "no_predefined_drift_detected"
        ),
        "notice": (
            "These keyword checks cannot establish whether a "
            "translation is accurate. Review both texts in context. "
            "The current drift rules primarily recognize English "
            "certainty words."
        )
    }


# ==========================================
# Interactive test
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("       AI TruthTrail - Translation Engine")
    print("=" * 50)

    print("\nSupported languages:")
    print(", ".join(SUPPORTED_LANGUAGES.keys()))

    text = input("\nEnter the text to translate: ")
    source = input("Enter the source language: ")
    target = input("Enter the target language: ")

    try:
        result = translate_text(text, source, target)

        print("\n========== TRANSLATION RESULT ==========")
        print("Original:", result["original_text"])
        print("Translated:", result["translated_text"])
        print("Status:", result["status"])

        # Drift analysis currently uses English wording rules.
        if source.strip().lower() == "english" and target.strip().lower() == "english":
            drift = analyze_translation_drift(
                result["original_text"],
                result["translated_text"]
            )

            print("\n========== DRIFT ANALYSIS ==========")
            print("Status:", drift["status"])
            print("Findings:", drift["finding_count"])

            for finding in drift["findings"]:
                print("\nType:", finding["type"])
                print("Details:", ", ".join(finding["details"]))
                print("Explanation:", finding["description"])

            print("\nNotice:", drift["notice"])

    except (ValueError, RuntimeError) as error:
        print("\nTranslation Error:", error)