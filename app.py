from flask import Flask, request, jsonify
from flask_cors import CORS

from nlp_engine import analyze_claims
from summarizer import summarize_text
from ocr_engine import extract_text_from_image
from context_engine import analyze_context
from evidence_engine import analyze_evidence
from source_engine import analyze_source
from news_engine import analyze_news,search_news as engine_search_news
from claim_history import add_claim_version, get_claim_history

from pathlib import Path
from werkzeug.utils import secure_filename
import tempfile
import os


app = Flask(__name__)
CORS(app)

# Maximum uploaded image size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tif", "tiff"}


@app.route("/")
def home():
    return "AI TruthTrail Backend is Running!"


# --------------------------------------------------
# 1. CLAIM COMPARISON
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(silent=True) or {}

        original = data.get("original_claim", "")
        later = data.get("later_claim", "")

        result = analyze_claims(original, later)

        return jsonify(result)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Claim analysis failed")
        return jsonify({
            "error": "Analysis failed. Please try again."
        }), 500


# --------------------------------------------------
# 2. TEXT SUMMARIZATION
# --------------------------------------------------

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json(silent=True) or {}

        text = data.get("text", "")
        max_sentences = data.get("max_sentences", 3)

        if not isinstance(text, str) or not text.strip():
            return jsonify({
                "error": "Please provide text to summarize."
            }), 400

        try:
            max_sentences = int(max_sentences)
        except (ValueError, TypeError):
            return jsonify({
                "error": "max_sentences must be an integer."
            }), 400

        if not 1 <= max_sentences <= 10:
            return jsonify({
                "error": "max_sentences must be between 1 and 10."
            }), 400

        result = summarize_text(
            text,
            max_sentences=max_sentences
        )

        return jsonify(result)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Summarization failed")
        return jsonify({
            "error": "Summarization failed. Please try again."
        }), 500


# --------------------------------------------------
# 3. SCREENSHOT OCR
# --------------------------------------------------

@app.route("/ocr", methods=["POST"])
def ocr():
    temporary_path = None

    try:
        if "image" not in request.files:
            return jsonify({
                "error": "Please upload an image using the 'image' field."
            }), 400

        image = request.files["image"]

        if not image.filename:
            return jsonify({
                "error": "No image was selected."
            }), 400

        safe_name = secure_filename(image.filename)
        extension = Path(safe_name).suffix.lower().lstrip(".")

        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            return jsonify({
                "error": "Unsupported image format."
            }), 400

        file_handle = tempfile.NamedTemporaryFile(
            suffix="." + extension,
            delete=False
        )
        temporary_path = file_handle.name
        file_handle.close()

        image.save(temporary_path)

        result = extract_text_from_image(temporary_path)

        return jsonify(result)

    except (ValueError, FileNotFoundError) as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("OCR failed")
        return jsonify({
            "error": "OCR failed. Please try another image."
        }), 500

    finally:
        if temporary_path and os.path.exists(temporary_path):
            try:
                os.remove(temporary_path)
            except OSError:
                app.logger.warning("Could not remove temporary OCR file.")


# --------------------------------------------------
# 4. MISSING CONTEXT DETECTOR
# --------------------------------------------------

@app.route("/context", methods=["POST"])
def context():
    try:
        data = request.get_json(silent=True) or {}

        original = data.get("original_claim", "")
        later = data.get("later_claim", "")

        result = analyze_context(original, later)

        return jsonify(result)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Context analysis failed")
        return jsonify({
            "error": "Context analysis failed. Please try again."
        }), 500


# --------------------------------------------------
# 5. EVIDENCE TRAIL
# --------------------------------------------------

@app.route("/evidence", methods=["POST"])
def evidence():
    try:
        data = request.get_json(silent=True) or {}

        result = analyze_evidence(
            claim=data.get("claim", ""),
            source=data.get("source", ""),
            quote=data.get("quote", ""),
            url=data.get("url", ""),
            date=data.get("date", ""),
            notes=data.get("notes", "")
        )

        return jsonify(result)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Evidence analysis failed")
        return jsonify({
            "error": "Evidence analysis failed. Please try again."
        }), 500


# --------------------------------------------------
# 6. SOURCE ANALYSIS
# --------------------------------------------------

@app.route("/source", methods=["POST"])
def source():
    try:
        data = request.get_json(silent=True) or {}

        result = analyze_source(
            source_name=data.get("source_name", ""),
            url=data.get("url", ""),
            publication_date=data.get("publication_date", ""),
            notes=data.get("notes", "")
        )

        return jsonify(result)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Source analysis failed")
        return jsonify({
            "error": "Source analysis failed. Please try again."
        }), 500


# --------------------------------------------------
# 7. NEWS ANALYSIS
# --------------------------------------------------

@app.route("/news-analysis", methods=["POST"])
def news_analysis():
    try:
        data = request.get_json(silent=True) or {}

        result = analyze_news(
            title=data.get("title", ""),
            article_text=data.get("article_text", ""),
            source=data.get("source", ""),
            url=data.get("url", ""),
            published_date=data.get("published_date", "")
        )

        return jsonify(result)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("News analysis failed")
        return jsonify({
            "error": "News analysis failed. Please try again."
        }), 500

# --------------------------------------------------
# NEWS SEARCH
# --------------------------------------------------

@app.route("/news-search", methods=["POST"])
def news_search():
    try:
        data = request.get_json(silent=True) or {}
        query = data.get("query", "")

        result =  engine_search_news(query)

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("News search failed")
        return jsonify({
            "error": "News search failed. Please try again."
        }), 500
# --------------------------------------------------
# 8. SAVE A CLAIM VERSION
# --------------------------------------------------

@app.route("/history", methods=["POST"])
def save_claim_history():
    try:
        data = request.get_json(silent=True) or {}

        result = add_claim_version(
            claim_id=data.get("claim_id", ""),
            claim_text=data.get("claim_text", ""),
            source=data.get("source", ""),
            notes=data.get("notes", "")
        )

        return jsonify({
            "message": "Claim version saved successfully.",
            "record": result
        }), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Saving claim history failed")
        return jsonify({
            "error": "Could not save claim history."
        }), 500


# --------------------------------------------------
# 9. GET CLAIM HISTORY
# --------------------------------------------------

@app.route("/history/<claim_id>", methods=["GET"])
def read_claim_history(claim_id):
    try:
        history = get_claim_history(claim_id)

        return jsonify({
            "claim_id": claim_id,
            "versions": history,
            "count": len(history)
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Reading claim history failed")
        return jsonify({
            "error": "Could not retrieve claim history."
        }), 500


# --------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------

@app.errorhandler(413)
def request_too_large(error):
    return jsonify({
        "error": "Uploaded file is too large. Maximum size is 10 MB."
    }), 413


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "API endpoint not found."
    }), 404


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_news(query, max_results=5):
    """Search recent news using the GNews API."""

    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key:
        raise ValueError(
            "GNews API key missing. Please check your .env file."
        )

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Please enter a news search query.")

    response = requests.get(
        "https://gnews.io/api/v4/search",
        params={
            "q": query.strip(),
            "lang": "en",
            "max": max_results,
            "apikey": api_key
        },
        timeout=20
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"News API request failed with status {response.status_code}."
        )

    data = response.json()

    return {
        "query": query,
        "total_articles": len(data.get("articles", [])),
        "articles": [
            {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", ""),
                "published_at": article.get("publishedAt", "")
            }
            for article in data.get("articles", [])
        ]
    }   