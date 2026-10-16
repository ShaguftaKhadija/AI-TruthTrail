
# import re
# import json
# from sentence_transformers import SentenceTransformer, util


# # 1. Load the pretrained NLP model once
# print("Loading NLP model...")

# model = SentenceTransformer("all-MiniLM-L6-v2")

# print("NLP Engine Ready!")


# # 2. Words and phrases used for rule-based analysis

# HEDGING_WORDS = {
#     "may", "might", "could", "possibly", "potentially",
#     "suggest", "suggests", "suggested", "appear", "appears",
#     "appeared", "seem", "seems", "likely", "unlikely",
#     "preliminary"
# }

# STRONG_WORDS = {
#     "proves", "prove", "proven", "confirmed",
#     "demonstrates", "demonstrate", "definitely",
#     "certainly", "undoubtedly"
# }

# CONTEXT_PHRASES = [
#     "early studies",
#     "preliminary research",
#     "according to researchers",
#     "according to the report",
#     "in some cases",
#     "in certain cases",
#     "among certain patients",
#     "in laboratory studies",
#     "in a small study",
#     "initial research",
#     "limited evidence",
#     "animal studies",
#     "in this study"
# ]

# LIMITING_WORDS = {
#     "some", "certain", "specific", "selected",
#     "limited", "individual", "particular", "few"
# }

# BROAD_WORDS = {
#     "all", "every", "everyone", "everybody",
#     "entire", "universal", "universally"
# }

# STOP_WORDS = {
#     "a", "an", "the", "is", "are", "was", "were",
#     "be", "been", "being", "of", "to", "in", "on",
#     "at", "for", "and", "or", "but", "that", "this",
#     "it", "as", "by", "with", "from", "into", "their",
#     "they", "them", "which", "who", "has", "have",
#     "had", "do", "does", "did"
# }


# def get_words(text):
#     """Convert text into lowercase words."""
#     return re.findall(r"\b[a-z]+\b", text.lower())


# def find_matching_words(text, word_set):
#     """Find words from a specified set."""
#     words = get_words(text)
#     return sorted(set(words) & word_set)


# # 3. Calculate semantic similarity

# def calculate_similarity(original, later):
#     embeddings = model.encode(
#         [original, later],
#         convert_to_tensor=True
#     )

#     score = util.cos_sim(
#         embeddings[0], embeddings[1]
#     ).item()

#     # Keep the displayed score between 0 and 100.
#     # This is a similarity indicator, not a truth score.
#     percentage = max(0.0, min(1.0, score)) * 100

#     return round(percentage, 2)


# # 4. Detect changes in certainty

# def detect_certainty_change(original, later):
#     original_words = get_words(original)
#     later_words = get_words(later)

#     original_hedges = find_matching_words(
#         original, HEDGING_WORDS
#     )
#     later_hedges = find_matching_words(
#         later, HEDGING_WORDS
#     )

#     original_strong = find_matching_words(
#         original, STRONG_WORDS
#     )
#     later_strong = find_matching_words(
#         later, STRONG_WORDS
#     )

#     # Also check common cautious phrases.
#     cautious_phrases = [
#         "studies suggest",
#         "study suggests",
#         "evidence suggests",
#         "may help",
#         "may reduce",
#         "might help",
#         "might reduce",
#         "could help",
#         "could reduce"
#     ]

#     original_cautious = [
#         phrase for phrase in cautious_phrases
#         if phrase in original.lower()
#     ]

#     later_cautious = [
#         phrase for phrase in cautious_phrases
#         if phrase in later.lower()
#     ]

#     if (
#         (original_hedges and not later_hedges)
#         or (original_cautious and not later_cautious)
#     ):
#         return {
#             "detected": True,
#             "type": "Certainty Increased",
#             "description": (
#                 "Cautious or uncertain wording in the original "
#                 "claim is missing from the later claim."
#             ),
#             "original_words": original_hedges,
#             "later_words": later_hedges
#         }

#     if original_strong and not later_strong:
#         return {
#             "detected": True,
#             "type": "Certainty Decreased",
#             "description": (
#                 "Strong certainty wording in the original "
#                 "claim is missing from the later claim."
#             ),
#             "original_words": original_strong,
#             "later_words": later_strong
#         }

#     return {
#         "detected": False,
#         "type": None,
#         "description": "No certainty shift detected by the rules."
#     }


# # 5. Detect removed or added context

# def detect_context_change(original, later):
#     original_lower = original.lower()
#     later_lower = later.lower()

#     removed = [
#         phrase for phrase in CONTEXT_PHRASES
#         if phrase in original_lower
#         and phrase not in later_lower
#     ]

#     added = [
#         phrase for phrase in CONTEXT_PHRASES
#         if phrase in later_lower
#         and phrase not in original_lower
#     ]

#     if removed:
#         return {
#             "detected": True,
#             "type": "Context Removed",
#             "description": (
#                 "Qualifying context present in the original "
#                 "claim is missing from the later claim."
#             ),
#             "removed_context": removed
#         }

#     if added:
#         return {
#             "detected": True,
#             "type": "Context Added",
#             "description": (
#                 "Additional qualifying context appears "
#                 "in the later claim."
#             ),
#             "added_context": added
#         }

#     return {
#         "detected": False,
#         "type": None,
#         "description": "No context phrase change detected."
#     }


# # 6. Detect possible changes in scope

# def detect_scope_change(original, later):
#     original_limited = find_matching_words(
#         original, LIMITING_WORDS
#     )
#     later_limited = find_matching_words(
#         later, LIMITING_WORDS
#     )

#     original_broad = find_matching_words(
#         original, BROAD_WORDS
#     )
#     later_broad = find_matching_words(
#         later, BROAD_WORDS
#     )

#     if (
#         (original_limited and not later_limited)
#         or (later_broad and not original_broad)
#     ):
#         return {
#             "detected": True,
#             "type": "Scope Changed",
#             "description": (
#                 "The later claim removes limiting language "
#                 "or introduces broader wording."
#             ),
#             "original_limiting_words": original_limited,
#             "later_limiting_words": later_limited,
#             "later_broad_words": later_broad
#         }

#     return {
#         "detected": False,
#         "type": None,
#         "description": (
#             "No scope change was detected by the basic rules."
#         )
#     }

# # ==========================================
# # NEGATION DETECTION
# # ==========================================

# NEGATION_WORDS = {
#     "not", "no", "never", "neither", "nor",
#     "cannot", "can't", "isn't", "aren't",
#     "wasn't", "weren't", "doesn't", "don't",
#     "didn't", "without", "unlikely"
# }


# def detect_negation_change(original, later):
#     original_words = set(get_words(original))
#     later_words = set(get_words(later))

#     original_negations = sorted(
#         original_words & NEGATION_WORDS
#     )

#     later_negations = sorted(
#         later_words & NEGATION_WORDS
#     )

#     if bool(original_negations) != bool(later_negations):
#         return {
#             "detected": True,
#             "type": "Negation Change",
#             "description": (
#                 "One claim contains negation-related wording "
#                 "that is missing from the other claim."
#             ),
#             "original_negations": original_negations,
#             "later_negations": later_negations
#         }

#     return {
#         "detected": False,
#         "type": None,
#         "description": "No basic negation change detected."
#     }


# # ==========================================
# # CONTRADICTION INDICATORS
# # ==========================================

# OPPOSITE_WORD_PAIRS = [
#     ("increase", "decrease"),
#     ("increases", "decreases"),
#     ("increased", "decreased"),
#     ("increasing", "decreasing"),
#     ("rise", "fall"),
#     ("rises", "falls"),
#     ("rose", "fell"),
#     ("higher", "lower"),
#     ("high", "low"),
#     ("more", "less"),
#     ("improve", "worsen"),
#     ("improves", "worsens"),
#     ("improved", "worsened"),
#     ("approved", "rejected"),
#     ("approve", "reject"),
#     ("safe", "unsafe"),
#     ("effective", "ineffective"),
#     ("positive", "negative"),
#     ("accept", "reject"),
#     ("accepted", "rejected")
# ]


# def detect_contradiction_indicators(original, later):
#     original_words = set(get_words(original))
#     later_words = set(get_words(later))

#     detected_pairs = []

#     for word_a, word_b in OPPOSITE_WORD_PAIRS:
#         if (
#             word_a in original_words
#             and word_b in later_words
#         ):
#             detected_pairs.append({
#                 "original_word": word_a,
#                 "later_word": word_b
#             })

#         elif (
#             word_b in original_words
#             and word_a in later_words
#         ):
#             detected_pairs.append({
#                 "original_word": word_b,
#                 "later_word": word_a
#             })

#     if detected_pairs:
#         return {
#             "detected": True,
#             "type": "Possible Contradiction",
#             "description": (
#                 "Potentially opposite terms were found "
#                 "in the two claims. Review the context "
#                 "before deciding whether they contradict."
#             ),
#             "opposite_terms": detected_pairs
#         }

#     return {
#         "detected": False,
#         "type": None,
#         "description": (
#             "No predefined opposite-word pair was detected."
#         )
#     }

# # 7. Compare meaningful words

# def compare_information(original, later):
#     original_words = {
#         word for word in get_words(original)
#         if word not in STOP_WORDS and len(word) > 1
#     }

#     later_words = {
#         word for word in get_words(later)
#         if word not in STOP_WORDS and len(word) > 1
#     }

#     return {
#         "added_words": sorted(later_words - original_words),
#         "removed_words": sorted(original_words - later_words)
#     }

# # 7.5 Detect changes in numbers, dates, and named entities

# def detect_key_detail_changes(original, later):
#     """
#     Identify differences in numbers, dates, and simple
#     capitalized named-entity phrases.

#     These are surface-level checks, not full fact verification.
#     """

#     # Extract numbers, including decimals and percentages
#     number_pattern = r"(?<!\w)\d+(?:,\d{3})*(?:\.\d+)?%?"

#     original_numbers = re.findall(number_pattern, original)
#     later_numbers = re.findall(number_pattern, later)

#     # Extract simple date-like expressions
#     date_pattern = (
#         r"\b(?:"
#         r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
#         r"|"
#         r"\d{4}-\d{2}-\d{2}"
#         r"|"
#         r"January|February|March|April|May|June|July|August|"
#         r"September|October|November|December"
#         r")\b"
#     )

#     original_dates = re.findall(
#         date_pattern, original, flags=re.IGNORECASE
#     )
#     later_dates = re.findall(
#         date_pattern, later, flags=re.IGNORECASE
#     )

#     # Detect simple capitalized names and organization-like phrases.
#     # This is a heuristic, not a full named-entity recognition model.
#     entity_pattern = (
#         r"\b[A-Z][a-z]+"
#         r"(?:\s+[A-Z][a-z]+){0,3}\b"
#     )

#     original_entities = re.findall(entity_pattern, original)
#     later_entities = re.findall(entity_pattern, later)

#     changes = []

#     if original_numbers != later_numbers:
#         changes.append({
#             "type": "Numbers Changed",
#             "original": original_numbers,
#             "later": later_numbers,
#             "description": (
#                 "The numerical details differ between the two claims."
#             )
#         })

#     if original_dates != later_dates:
#         changes.append({
#             "type": "Dates Changed",
#             "original": original_dates,
#             "later": later_dates,
#             "description": (
#                 "The date-like expressions differ between the two claims."
#             )
#         })

#     if set(original_entities) != set(later_entities):
#         changes.append({
#             "type": "Named Entities Changed",
#             "original": sorted(set(original_entities)),
#             "later": sorted(set(later_entities)),
#             "description": (
#                 "Some capitalized names or phrases differ between claims."
#             )
#         })

#     return changes

# # 8. Main function: combine all analysis

# def analyze_claims(original, later):
#     if not isinstance(original, str) or not isinstance(later, str):
#         raise ValueError("Both claims must be text.")

#     original = original.strip()
#     later = later.strip()

#     if not original or not later:
#         raise ValueError("Please enter both claims.")

#   similarity = calculate_similarity(original, later)

# certainty = detect_certainty_change(original, later)
# context = detect_context_change(original, later)
# scope = detect_scope_change(original, later)
# information = compare_information(original, later)

# key_detail_changes = detect_key_detail_changes(
#     original, later
# )

# negation = detect_negation_change(
#     original, later
# )

# contradiction = detect_contradiction_indicators(
#     original, later
# )
#    changes = []

# for result in [
#     certainty,
#     context,
#     scope,
#     negation,
#     contradiction
# ]:
#     if result["detected"]:
#         changes.append(result)

# changes.extend(key_detail_changes)
# changes.extend(key_detail_changes)

#     if information["added_words"]:
#         changes.append({
#             "detected": True,
#             "type": "Information Added",
#             "description": (
#                 "The later claim contains words not present "
#                 "in the original claim."
#             ),
#             "words": information["added_words"]
#         })

#     if information["removed_words"]:
#         changes.append({
#             "detected": True,
#             "type": "Information Removed",
#             "description": (
#                 "Words from the original claim are missing "
#                 "from the later claim."
#             ),
#             "words": information["removed_words"]
#         })

#     return {
#         "similarity": similarity,
#         "similarity_label": (
#             "Highly Similar" if similarity >= 80
#             else "Moderately Similar" if similarity >= 50
#             else "Less Similar"
#         ),
#         "changes": changes,
#         "information_comparison": information
#     }


# # 9. Run a sample test when this file is executed directly

# if __name__ == "__main__":
#     original_claim = (
#         "Early studies suggest that green tea may reduce "
#         "certain cardiovascular risk factors."
#     )

#     later_claim = "Green tea reduces heart disease."

#     result = analyze_claims(original_claim, later_claim)

#     print("\n--- AI TruthTrail NLP Test ---")
#     print(json.dumps(result, indent=4))


import re
import json
from sentence_transformers import SentenceTransformer, util


# Load the pretrained NLP model once.
print("Loading NLP model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("NLP Engine Ready!")


HEDGING_WORDS = {
    "may", "might", "could", "possibly", "potentially",
    "suggest", "suggests", "suggested", "appear", "appears",
    "appeared", "seem", "seems", "likely", "unlikely",
    "preliminary",
}

STRONG_WORDS = {
    "proves", "prove", "proven", "confirmed",
    "demonstrates", "demonstrate", "definitely",
    "certainly", "undoubtedly",
}

CONTEXT_PHRASES = [
    "early studies", "preliminary research", "according to researchers",
    "according to the report", "in some cases", "in certain cases",
    "among certain patients", "in laboratory studies", "in a small study",
    "initial research", "limited evidence", "animal studies", "in this study",
]

LIMITING_WORDS = {
    "some", "certain", "specific", "selected", "limited",
    "individual", "particular", "few",
}

BROAD_WORDS = {
    "all", "every", "everyone", "everybody", "entire",
    "universal", "universally",
}

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "being", "of", "to", "in", "on", "at", "for", "and", "or",
    "but", "that", "this", "it", "as", "by", "with", "from",
    "into", "their", "they", "them", "which", "who", "has",
    "have", "had", "do", "does", "did",
}


def get_words(text):
    """Convert text into lowercase words."""
    return re.findall(r"\b[a-z]+\b", text.lower())


def find_matching_words(text, word_set):
    """Find words from a specified set."""
    return sorted(set(get_words(text)) & word_set)


def calculate_similarity(original, later):
    """Calculate semantic similarity as a percentage."""
    embeddings = model.encode([original, later], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    # Similarity indicator only; it is not a truth score.
    percentage = max(0.0, min(1.0, score)) * 100
    return round(percentage, 2)


def detect_certainty_change(original, later):
    original_hedges = find_matching_words(original, HEDGING_WORDS)
    later_hedges = find_matching_words(later, HEDGING_WORDS)
    original_strong = find_matching_words(original, STRONG_WORDS)
    later_strong = find_matching_words(later, STRONG_WORDS)

    cautious_phrases = [
        "studies suggest", "study suggests", "evidence suggests",
        "may help", "may reduce", "might help", "might reduce",
        "could help", "could reduce",
    ]
    original_cautious = [
        phrase for phrase in cautious_phrases if phrase in original.lower()
    ]
    later_cautious = [
        phrase for phrase in cautious_phrases if phrase in later.lower()
    ]

    if ((original_hedges and not later_hedges)
            or (original_cautious and not later_cautious)):
        return {
            "detected": True,
            "type": "Certainty Increased",
            "description": (
                "Cautious or uncertain wording in the original claim "
                "is missing from the later claim."
            ),
            "original_words": original_hedges,
            "later_words": later_hedges,
        }

    if original_strong and not later_strong:
        return {
            "detected": True,
            "type": "Certainty Decreased",
            "description": (
                "Strong certainty wording in the original claim "
                "is missing from the later claim."
            ),
            "original_words": original_strong,
            "later_words": later_strong,
        }

    return {
        "detected": False,
        "type": None,
        "description": "No certainty shift detected by the rules.",
    }


def detect_context_change(original, later):
    original_lower = original.lower()
    later_lower = later.lower()
    removed = [
        phrase for phrase in CONTEXT_PHRASES
        if phrase in original_lower and phrase not in later_lower
    ]
    added = [
        phrase for phrase in CONTEXT_PHRASES
        if phrase in later_lower and phrase not in original_lower
    ]

    if removed:
        return {
            "detected": True,
            "type": "Context Removed",
            "description": (
                "Qualifying context present in the original claim "
                "is missing from the later claim."
            ),
            "removed_context": removed,
        }
    if added:
        return {
            "detected": True,
            "type": "Context Added",
            "description": "Additional qualifying context appears in the later claim.",
            "added_context": added,
        }
    return {
        "detected": False,
        "type": None,
        "description": "No context phrase change detected.",
    }


def detect_scope_change(original, later):
    original_limited = find_matching_words(original, LIMITING_WORDS)
    later_limited = find_matching_words(later, LIMITING_WORDS)
    original_broad = find_matching_words(original, BROAD_WORDS)
    later_broad = find_matching_words(later, BROAD_WORDS)

    if ((original_limited and not later_limited)
            or (later_broad and not original_broad)):
        return {
            "detected": True,
            "type": "Scope Changed",
            "description": (
                "The later claim removes limiting language "
                "or introduces broader wording."
            ),
            "original_limiting_words": original_limited,
            "later_limiting_words": later_limited,
            "later_broad_words": later_broad,
        }
    return {
        "detected": False,
        "type": None,
        "description": "No scope change was detected by the basic rules.",
    }


NEGATION_WORDS = {
    "not", "no", "never", "neither", "nor", "cannot", "can't",
    "isn't", "aren't", "wasn't", "weren't", "doesn't", "don't",
    "didn't", "without", "unlikely",
}


def detect_negation_change(original, later):
    original_words = set(get_words(original))
    later_words = set(get_words(later))
    original_negations = sorted(original_words & NEGATION_WORDS)
    later_negations = sorted(later_words & NEGATION_WORDS)

    if bool(original_negations) != bool(later_negations):
        return {
            "detected": True,
            "type": "Negation Change",
            "description": (
                "One claim contains negation-related wording "
                "that is missing from the other claim."
            ),
            "original_negations": original_negations,
            "later_negations": later_negations,
        }
    return {
        "detected": False,
        "type": None,
        "description": "No basic negation change detected.",
    }


OPPOSITE_WORD_PAIRS = [
    ("increase", "decrease"), ("increases", "decreases"),
    ("increased", "decreased"), ("increasing", "decreasing"),
    ("rise", "fall"), ("rises", "falls"), ("rose", "fell"),
    ("higher", "lower"), ("high", "low"), ("more", "less"),
    ("improve", "worsen"), ("improves", "worsens"),
    ("improved", "worsened"), ("approved", "rejected"),
    ("approve", "reject"), ("safe", "unsafe"),
    ("effective", "ineffective"), ("positive", "negative"),
    ("accept", "reject"), ("accepted", "rejected"),
]


def detect_contradiction_indicators(original, later):
    original_words = set(get_words(original))
    later_words = set(get_words(later))
    detected_pairs = []

    for word_a, word_b in OPPOSITE_WORD_PAIRS:
        if word_a in original_words and word_b in later_words:
            detected_pairs.append({"original_word": word_a, "later_word": word_b})
        elif word_b in original_words and word_a in later_words:
            detected_pairs.append({"original_word": word_b, "later_word": word_a})

    if detected_pairs:
        return {
            "detected": True,
            "type": "Possible Contradiction",
            "description": (
                "Potentially opposite terms were found in the two claims. "
                "Review the context before deciding whether they contradict."
            ),
            "opposite_terms": detected_pairs,
        }
    return {
        "detected": False,
        "type": None,
        "description": "No predefined opposite-word pair was detected.",
    }


def compare_information(original, later):
    original_words = {
        word for word in get_words(original)
        if word not in STOP_WORDS and len(word) > 1
    }
    later_words = {
        word for word in get_words(later)
        if word not in STOP_WORDS and len(word) > 1
    }
    return {
        "added_words": sorted(later_words - original_words),
        "removed_words": sorted(original_words - later_words),
    }


def detect_key_detail_changes(original, later):
    """Find surface-level differences in numbers, dates, and names."""
    number_pattern = r"(?<!\w)\d+(?:,\d{3})*(?:\.\d+)?%?"
    original_numbers = re.findall(number_pattern, original)
    later_numbers = re.findall(number_pattern, later)

    date_pattern = (
        r"\b(?:"
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|\d{4}-\d{2}-\d{2}"
        r"|January|February|March|April|May|June|July|August|"
        r"September|October|November|December"
        r")\b"
    )
    original_dates = re.findall(date_pattern, original, flags=re.IGNORECASE)
    later_dates = re.findall(date_pattern, later, flags=re.IGNORECASE)

    entity_pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\b"
    original_entities = re.findall(entity_pattern, original)
    later_entities = re.findall(entity_pattern, later)

    changes = []
    if original_numbers != later_numbers:
        changes.append({
            "detected": True,
            "type": "Numbers Changed",
            "original": original_numbers,
            "later": later_numbers,
            "description": "The numerical details differ between the two claims.",
        })
    if original_dates != later_dates:
        changes.append({
            "detected": True,
            "type": "Dates Changed",
            "original": original_dates,
            "later": later_dates,
            "description": "The date-like expressions differ between the two claims.",
        })
    if set(original_entities) != set(later_entities):
        changes.append({
            "detected": True,
            "type": "Named Entities Changed",
            "original": sorted(set(original_entities)),
            "later": sorted(set(later_entities)),
            "description": "Some capitalized names or phrases differ between claims.",
        })
    return changes


def analyze_claims(original, later):
    """Compare two claims and return similarity and possible changes."""
    if not isinstance(original, str) or not isinstance(later, str):
        raise ValueError("Both claims must be text.")

    original = original.strip()
    later = later.strip()
    if not original or not later:
        raise ValueError("Please enter both claims.")

    similarity = calculate_similarity(original, later)
    certainty = detect_certainty_change(original, later)
    context = detect_context_change(original, later)
    scope = detect_scope_change(original, later)
    information = compare_information(original, later)
    key_detail_changes = detect_key_detail_changes(original, later)
    negation = detect_negation_change(original, later)
    contradiction = detect_contradiction_indicators(original, later)

    changes = []
    for result in [certainty, context, scope, negation, contradiction]:
        if result["detected"]:
            changes.append(result)

    # Add number/date/name differences exactly once.
    changes.extend(key_detail_changes)

    if information["added_words"]:
        changes.append({
            "detected": True,
            "type": "Information Added",
            "description": (
                "The later claim contains words not present in the original claim."
            ),
            "words": information["added_words"],
        })
    if information["removed_words"]:
        changes.append({
            "detected": True,
            "type": "Information Removed",
            "description": (
                "Words from the original claim are missing from the later claim."
            ),
            "words": information["removed_words"],
        })

    return {
        "similarity": similarity,
        "similarity_label": (
            "Highly Similar" if similarity >= 80
            else "Moderately Similar" if similarity >= 50
            else "Less Similar"
        ),
        "changes": changes,
        "information_comparison": information,
    }


if __name__ == "__main__":
    original_claim = (
        "Early studies suggest that green tea may reduce "
        "certain cardiovascular risk factors."
    )
    later_claim = "Green tea reduces heart disease."
    result = analyze_claims(original_claim, later_claim)
    print("\n--- AI TruthTrail NLP Test ---")
    print(json.dumps(result, indent=4))
