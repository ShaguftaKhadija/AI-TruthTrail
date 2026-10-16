import re


def summarize_text(text, max_sentences=3):
    """
    Generate a short extractive summary from the provided text.

    Args:
        text (str): Text to summarize.
        max_sentences (int): Maximum number of sentences in the summary.

    Returns:
        dict: Summary and basic statistics.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please provide some text to summarize.")

    if not isinstance(max_sentences, int) or isinstance(max_sentences, bool):
        raise ValueError("max_sentences must be an integer.")

    if not 1 <= max_sentences <= 10:
        raise ValueError("max_sentences must be between 1 and 10.")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split the text into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if not sentences:
        raise ValueError("No valid sentences found in the text.")

    # Return the original text if it is already short
    if len(sentences) <= max_sentences:
        summary = " ".join(sentences)

    else:
        # Remove common words when calculating sentence importance
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were",
            "in", "on", "at", "to", "of", "and", "or",
            "for", "with", "by", "as", "it", "this",
            "that", "from", "be", "has", "have", "had"
        }

        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        frequencies = {}

        for word in words:
            if word not in stop_words:
                frequencies[word] = frequencies.get(word, 0) + 1

        scored_sentences = []

        for index, sentence in enumerate(sentences):
            sentence_words = re.findall(
                r"\b[a-zA-Z]+\b",
                sentence.lower()
            )

            important_words = [
                word for word in sentence_words
                if word not in stop_words
            ]

            score = sum(
                frequencies.get(word, 0)
                for word in important_words
            )

            if important_words:
                score = score / len(important_words)

            scored_sentences.append((index, score, sentence))

        # Select the highest-scoring sentences
        selected = sorted(
            scored_sentences,
            key=lambda item: item[1],
            reverse=True
        )[:max_sentences]

        # Restore their original order
        selected.sort(key=lambda item: item[0])

        summary = " ".join(
            sentence for _, _, sentence in selected
        )

    return {
        "summary": summary,
        "original_sentence_count": len(sentences),
        "summary_sentence_count": len(
            re.split(r"(?<=[.!?])\s+", summary)
        )
    }