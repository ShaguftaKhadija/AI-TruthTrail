# from summarizer import summarize_text


# text = """
# Climate change is affecting weather patterns around the world.
# Rising temperatures are contributing to the melting of glaciers.
# Scientists are studying these changes to understand their long-term effects.
# Governments are developing policies to reduce greenhouse gas emissions.
# Renewable energy is one approach to reducing emissions.
# """

# result = summarize_text(text, max_sentences=2)

# print("Summary:")
# print(result["summary"])

# print("\nOriginal sentences:", result["original_sentence_count"])
# print("Summary sentences:", result["summary_sentence_count"])

from summarizer import summarize_text

print("===== AI TruthTrail Summarizer Test =====")

text = input("\nEnter the text you want to summarize:\n\n")

if not text.strip():
    print("Please enter some text.")
else:
    try:
        result = summarize_text(text, max_sentences=3)

        print("\n===== Summary =====")
        print(result["summary"])

        print("\nOriginal sentences:",
              result["original_sentence_count"])

        print("Summary sentences:",
              result["summary_sentence_count"])

    except ValueError as error:
        print("Error:", error)
