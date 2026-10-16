import re


# ==========================================
# AI TruthTrail - Context Analysis Engine
# ==========================================

# Words that may limit or qualify a claim
LIMITING_WORDS = {
    "some", "certain", "specific", "selected",
    "limited", "individual", "particular", "few",
    "occasionally", "sometimes", "partially"
}

# Words that may broaden a claim
BROAD_WORDS = {
    "all", "every", "everyone", "everybody",
    "entire", "universally", "always", "never"
}

# Phrases that may provide important context
CONTEXT_PHRASES = [
    "early studies",
    "preliminary research",
    "according to researchers",
    "according to the report",
    "in some cases",
    "in certain cases",
    "among certain patients",
    "in laboratory studies",
    "in a small study",
    "initial research",
    "limited evidence",
    "animal studies",
    "in this study",
    "under certain conditions",
    "in the short term",
    "in the long term",
    "according to the study",
    "research suggests",
    "studies suggest",
    "may help",
    "might help",
    "could help",
    "may reduce",
    "might reduce",
    "could reduce"
]

# Words that may express uncertainty
UNCERTAINTY_WORDS = {
    "may", "might", "could", "possibly",
    "potentially", "likely", "unlikely",
    "suggest", "suggests", "suggested",
    "appears", "appear", "seems", "seem",
    "preliminary"
}


def clean_text(text):
    """Normalize text for basic context analysis."""

    if not isinstance(text, str):
        return ""

    return re.sub(r"\s+", " ", text.strip()).lower()


def find_matching_words(text, word_set):
    """Find words from a predefined set."""

    words = set(re.findall(r"\b[\w'-]+\b", text.lower()))

    return sorted(words.intersection(word_set))


def find_context_phrases(text):
    """Find predefined context phrases in text."""

    text = clean_text(text)

    return [
        phrase
        for phrase in CONTEXT_PHRASES
        if re.search(
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)",
            text
        )
    ]


def detect_missing_qualifiers(original, later):
    """
    Identify qualifiers present in the original claim
    but missing from the later claim.
    """

    original = clean_text(original)
    later = clean_text(later)

    original_limiters = find_matching_words(
        original, LIMITING_WORDS
    )

    later_limiters = find_matching_words(
        later, LIMITING_WORDS
    )

    removed_limiters = sorted(
        set(original_limiters) - set(later_limiters)
    )

    original_context = find_context_phrases(original)
    later_context = find_context_phrases(later)

    removed_context = sorted(
        set(original_context) - set(later_context)
    )

    original_uncertainty = find_matching_words(
        original, UNCERTAINTY_WORDS
    )

    later_uncertainty = find_matching_words(
        later, UNCERTAINTY_WORDS
    )

    removed_uncertainty = sorted(
        set(original_uncertainty) - set(later_uncertainty)
    )

    findings = []

    if removed_limiters:
        findings.append({
            "type": "Limiting Detail Removed",
            "details": removed_limiters,
            "description": (
                "Words that may limit the scope of the original "
                "claim are missing from the later claim."
            )
        })

    if removed_context:
        findings.append({
            "type": "Context Phrase Removed",
            "details": removed_context,
            "description": (
                "A contextual phrase in the original claim "
                "is missing from the later claim."
            )
        })

    if removed_uncertainty:
        findings.append({
            "type": "Uncertainty Wording Removed",
            "details": removed_uncertainty,
            "description": (
                "The later claim omits wording that may express "
                "uncertainty in the original claim."
            )
        })

    return findings


def detect_broadened_claim(original, later):
    """
    Identify possible broadening of a claim.

    This checks predefined wording only. It does not prove
    that the meaning has actually broadened.
    """

    original = clean_text(original)
    later = clean_text(later)

    original_broad = find_matching_words(
        original, BROAD_WORDS
    )

    later_broad = find_matching_words(
        later, BROAD_WORDS
    )

    newly_added_broad_words = sorted(
        set(later_broad) - set(original_broad)
    )

    if newly_added_broad_words:
        return {
            "detected": True,
            "type": "Potentially Broadened Claim",
            "words": newly_added_broad_words,
            "description": (
                "The later claim introduces words that may make "
                "the statement broader or more absolute."
            )
        }

    return {
        "detected": False,
        "type": None,
        "words": [],
        "description": (
            "No new predefined broadening words were detected."
        )
    }


def analyze_context(original, later):
    """
    Compare two claims and return possible contextual changes.
    """

    if not isinstance(original, str) or not isinstance(later, str):
        raise ValueError("Both claims must be text.")

    original = original.strip()
    later = later.strip()

    if not original:
        raise ValueError("Please provide the original claim.")

    if not later:
        raise ValueError("Please provide the later claim.")

    missing_qualifiers = detect_missing_qualifiers(
        original, later
    )

    broadening = detect_broadened_claim(
        original, later
    )

    return {
        "original_claim": original,
        "later_claim": later,
        "missing_qualifiers": missing_qualifiers,
        "broadened_claim": broadening,
        "finding_count": (
            len(missing_qualifiers)
            + int(broadening["detected"])
        ),
        "status": (
            "potential_context_changes_detected"
            if missing_qualifiers or broadening["detected"]
            else "no_predefined_context_changes_detected"
        ),
        "notice": (
            "These are rule-based indicators, not proof of "
            "misinformation. Review the full context before "
            "drawing conclusions."
        )
    }


# ==========================================
# Standalone test
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("       AI TruthTrail - Context Analysis")
    print("=" * 50)

    original = input("\nEnter the original claim: ")
    later = input("Enter the later claim: ")

    try:
        result = analyze_context(original, later)

        print("\n========== CONTEXT ANALYSIS ==========")

        print("\nStatus:", result["status"])

        print(
            "Potential findings:",
            result["finding_count"]
        )

        if result["missing_qualifiers"]:
            print("\n--- Possible Missing Context ---")

            for finding in result["missing_qualifiers"]:
                print("\nType:", finding["type"])
                print("Details:", ", ".join(finding["details"]))
                print("Explanation:", finding["description"])

        broadening = result["broadened_claim"]

        if broadening["detected"]:
            print("\n--- Possible Claim Broadening ---")
            print("Words:", ", ".join(broadening["words"]))
            print("Explanation:", broadening["description"])

        if result["finding_count"] == 0:
            print("\nNo predefined context changes were detected.")

        print("\nNotice:", result["notice"])

    except ValueError as error:
        print("\nInput Error:", error)