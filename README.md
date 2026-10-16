
<div align="center">

# 🔎 AI TruthTrail

### Follow the Story Behind a Claim.

**Compare Claims · Screenshot OCR · Claim Timeline · Text Summarization**

Explore how information changes through wording, context, certainty, and meaning.

*One claim. Different versions. A closer look at the story.*

</div>

---

## 📑 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [Application Preview](#-application-preview)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Future Scope](#-future-scope)
- [Limitations](#-limitations)
- [Developer](#-developer)
- [Contributors](#-contributors)
- [License](#-license)

---

## 🌍 About the Project

Information can change as it travels.

A statement may be shortened, repeated without its original context, or presented with different wording and levels of certainty. Understanding these changes can be difficult when information appears across news articles, screenshots, and online sources.

**AI TruthTrail** is an NLP-based web application designed to help users compare claims, summarize lengthy information, examine potential changes in meaning, and explore the evolution of statements.

By bringing these capabilities together in one platform, AI TruthTrail encourages users to look beyond the surface of a statement and examine the context behind it.

Our goal is simple:

**Help people explore information, recognize potential meaning shifts, and ask better questions before sharing what they read.**

---

## 🎯 Problem Statement

Online information is often lengthy, fragmented, or presented differently across sources. Manually comparing claims, identifying changes in wording, and understanding missing context can be time-consuming.

Users need accessible tools to examine statements, summarize information, and investigate potential changes in meaning.

## 💡 Our Solution

AI TruthTrail combines claim comparison, text summarization, context-oriented analysis, screenshot text extraction, and claim evolution exploration in one web application.

The platform helps users:

- Compare two versions of a claim.
- Examine semantic similarity and potential meaning shifts.
- Identify possible changes in context and certainty.
- Summarize lengthy text into concise information.
- Extract text from screenshots using OCR.
- Explore changes in claims across available versions or sources.

**AI TruthTrail supports information analysis; it does not automatically determine whether a claim is true or false.**

---

## ✨ Key Features

### 🔍 1. Compare Claims

Compare an original statement with a later version and examine their similarities and potential differences.

**Features:**
- Semantic similarity score.
- Comparison of two claims.
- Detection of potential changes in wording.
- Identification of potentially missing qualifying language.
- Context and certainty difference indicators.
- Explanations of possible meaning shifts.

The comparison results help users investigate whether two statements communicate the same meaning or contain potentially important differences.

*Similarity scores are analytical indicators, not proof of factual accuracy.*

### 📰 2. TruthBrief — Text Summarization

TruthBrief helps users understand lengthy text or news content through concise summaries.

**Features:**
- Extraction of important sentences.
- Key sentence presentation.
- Quick extractive summaries.
- Readable presentation of summarized information.

By highlighting important sentences and generating a shorter version of the submitted text, TruthBrief helps users review lengthy information more efficiently.

Summaries should be checked against the original content to avoid missing important context.

### 📸 3. Screenshot OCR

Screenshot OCR is designed to extract readable text from supported images using Optical Character Recognition.

**Workflow:**

Upload Screenshot → Extract Text → Review Extracted Text → Analyze Content

This capability can help users work with information captured in screenshots, digital posts, and article images.

OCR results may contain errors when images are blurry, poorly lit, or contain complex layouts.

### 🧬 4. Claim Evolution Timeline

The Timeline feature is designed to organize available claim versions and help users explore how statements may change over time.

Potential areas of examination include:

- Changes in wording.
- Differences in context.
- Changes in certainty or scope.
- Relationships between different claim versions.
- Available dates and source information.

The usefulness of a timeline depends on the claim records and source information available to the application.

### 🧠 5. Context and Meaning Analysis

AI TruthTrail includes context-oriented analysis intended to identify potential differences between statements.

These may include:

- Missing qualifications.
- Changes in certainty.
- Broader or narrower wording.
- Differences in contextual meaning.
- Potentially important changes in scope.

The objective is to help users investigate differences that might otherwise be overlooked.

### 🌐 6. News and Source Exploration

The project includes news-search and source-related modules intended to support further exploration of information.

These capabilities can help users investigate related information and examine available sources.

Results depend on the configured services, available data, and the implementation of each module.

---

## 🖥️ Application Preview

The following screenshots showcase the AI TruthTrail interface and examples of its analysis results.

### 🏠 Homepage

![AI TruthTrail Homepage](screenshots/homepage.png.png)

*Follow the story behind a claim.*

### 🔍 Compare Claims

![AI TruthTrail Compare Claims](screenshots/compare.png.png)

The comparison interface displays semantic similarity and potential differences between two versions of a statement.

### 📰 TruthBrief — Summarization

![AI TruthTrail TruthBrief](screenshots/truthbrief.png.png)

The summarization interface presents key sentences alongside a quick extractive summary.

**To display these images on GitHub:**

1. Create a folder named `screenshots` in your repository.
2. Upload your homepage screenshot as `homepage.png`.
3. Upload your comparison screenshot as `compare.png`.
4. Upload your summarization screenshot as `truthbrief.png`.

Make sure the filenames match the paths used above.

---

## 🔄 How It Works

### Claim Comparison

1. Enter the original claim.
2. Enter the later version of the claim.
3. Submit both statements for analysis.
4. Review the semantic similarity score.
5. Examine the potential changes identified by the analysis.
6. Investigate the original sources when necessary.

### Text Summarization

1. Submit supported text or news content.
2. Process the text through the summarization component.
3. Review the extracted key sentences.
4. Read the quick summary.
5. Refer to the original content for additional context.

### Screenshot OCR

1. Select a supported screenshot.
2. Extract text using the OCR component.
3. Review the extracted text for errors.
4. Use the text for further analysis where supported.

### Claim Timeline

1. Review available claim records.
2. Examine different versions of a statement.
3. Compare potential changes in wording and context.
4. Investigate available dates and sources.

The availability of each workflow depends on the corresponding implementation and input data.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML |
| Styling | CSS |
| Interactive Functionality | JavaScript |
| Backend | Python, Flask |
| NLP | Sentence Transformers and text-analysis techniques |
| OCR | Configured OCR engine |
| Version Control | Git, GitHub |
| Development Environment | Visual Studio Code |

The final dependency list should match the libraries and services used in the project.

---

## 📁 Project Structure

The following structure is based on the files visible in the project's development environment.

```text
AI-TruthTrail/
│
├── app.py
├── index.html
├── script.js
├── style.css
│
├── nlp_engine.py
├── context_engine.py
├── evidence_eng.py
├── evidence_engine.py
├── news_engine.py
├── ocr_engine.py
├── source_engine.py
├── summarizer.py
├── translation_engine.py
│
├── claim_history.py
├── claim_history.json
│
├── check_translation.py
├── test_evidence.py
├── test_source.py
├── test_summarizer.py
│
├── requirements.txt
├── sample.txt
├── ocr_test.png
├── .gitignore
├── LICENSE
├── README.md
│
└── screenshots/
    ├── homepage.png
    ├── compare.png
    └── truthbrief.png
```

*Note: This is a reference structure based on the visible filenames. Verify the actual repository before treating it as the final directory structure.*

---

## 🚀 Getting Started

Follow these steps to run AI TruthTrail locally.

### Prerequisites

- Python 3
- pip
- Git
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/ShaguftaKhadija/AI-TruthTrail.git
```

### 2. Open the Project Folder

```bash
cd AI-TruthTrail
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

If the application requires API keys or other environment variables, configure them locally according to the project setup.

**Never commit API keys, passwords, or other secret credentials to GitHub.**

### 7. Start the Application

```bash
python app.py
```

Open the local address shown in the terminal.

*These instructions assume that `app.py` starts the Flask application and that `requirements.txt` contains the required dependencies. Additional configuration may be necessary.*

---

## 🔮 Future Scope

AI TruthTrail can be extended with additional capabilities:

- **Enhanced OCR:** Improve text extraction from low-quality screenshots.
- **Claim DNA:** Break statements into components such as who, what, when, scope, and certainty.
- **Expanded Claim Comparison:** Compare multiple statements from different sources.
- **Advanced Timeline Visualization:** Display changes across dated claim versions.
- **Multilingual Analysis:** Support additional languages.
- **Improved Source Exploration:** Make source information easier to examine.
- **Analysis History:** Improve access to previous comparisons and summaries.
- **Accessibility Enhancements:** Improve usability across devices and user needs.

These are potential enhancements, not claims that every capability is already implemented.

---

## ⚠️ Limitations and Responsible Use

AI TruthTrail is designed to support information analysis, not replace independent verification.

- Semantic similarity does not establish factual truth.
- Summaries may omit important information.
- OCR can misread text in images.
- Context analysis may produce incorrect interpretations.
- Timeline accuracy depends on the quality of available records.
- News and source results depend on the configured services.

Users should consult original sources and independently verify important information before making decisions.

---

## 👩‍💻 Developer

### Shagufta Khadija

**Developer — AI TruthTrail**

Responsible for developing the project and bringing its interface, claim analysis, text summarization, and related components together into a unified application.

GitHub: [@ShaguftaKhadija](https://github.com/ShaguftaKhadija)

---

## 🤝 Contributors

AI TruthTrail is a collaborative project built through teamwork, shared ideas, experimentation, and a common interest in making information easier to explore.

We gratefully acknowledge the contributions of the following team members:

| S. No. | Contributor |
|:---:|---|
| 1 | Zaheen Fatima |
| 2 | Khadeeja Afreen |
| 3 | Roquiya Basher |
| 4 | Muskan Khatun |
| 5 | Alisha Fatima |

Thank you to all contributors for being part of the AI TruthTrail project.

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for the complete license text.

---

<div align="center">

### 🔎 AI TruthTrail

**Follow the claim. Explore the context. Understand the change.**

*Built with curiosity, collaboration, and a commitment to more thoughtful information analysis.*

</div>
