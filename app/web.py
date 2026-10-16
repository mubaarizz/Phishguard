from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from flask import Flask, render_template, request, abort
from werkzeug.utils import secure_filename

from app.core.email_parser import parse_email
from app.core.header_analyzer import analyze_headers
from app.core.url_analyzer import analyze_url
from app.core.ml_analyzer import analyze_email_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

REPORTS = {}


@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html",
        error="File is too large. Maximum supported size is 10 MB.",
    ), 413


def analyze_uploaded_email(file_path):
    email = parse_email(file_path)

    ml_result = None
    ml_error = None

    try:
        ml_result = analyze_email_text(email["subject"], email["body"])
    except Exception as error:
        ml_error = f"ML analysis unavailable: {error}"

    url_results = [
        analyze_url(item["url"])
        for item in email["urls"]
    ]

    return {
        "email": email,
        "ml": ml_result,
        "ml_error": ml_error,
        "url_results": url_results,
        "header_analysis": email["header_analysis"],
        "headers": email["headers"],
        "report_id": uuid4().hex,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    uploaded_file = request.files.get("email_file")

    if not uploaded_file or not uploaded_file.filename:
        return render_template(
            "index.html",
            error="Please select an .eml file first.",
        ), 400

    filename = secure_filename(uploaded_file.filename)

    if not filename.lower().endswith(".eml"):
        return render_template(
            "index.html",
            error="Unsupported file type. Please upload an .eml file.",
        ), 400

    temp_path = None

    try:
        with NamedTemporaryFile(suffix=".eml", delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            uploaded_file.save(temp_path)

        if temp_path.stat().st_size == 0:
            return render_template(
                "index.html",
                error="The selected file is empty.",
            ), 400

        result = analyze_uploaded_email(temp_path)
        result["email"]["file_name"] = filename
        REPORTS[result["report_id"]] = result

        return render_template("result.html", result=result)

    except (OSError, ValueError) as error:
        return render_template(
            "index.html",
            error=f"Could not analyze this email: {error}",
        ), 400
    except Exception:
        app.logger.exception("Email analysis failed")
        return render_template(
            "index.html",
            error="Analysis failed. Check the terminal for technical details.",
        ), 500
    finally:
        if temp_path:
            temp_path.unlink(missing_ok=True)


@app.route("/report/<report_id>")
def download_report(report_id):
    result = REPORTS.get(report_id)

    if result is None:
        abort(404)

    response = app.make_response(
        render_template("report.html", result=result)
    )
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["Content-Disposition"] = (
        'attachment; filename="PHISHGUARD_Report.html"'
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
