from flask import Flask, request, jsonify
from flask_cors import CORS
from services.resume_processor import process_resume

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Process uploaded resume and return ranking."""
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_desc", "")

    ranking_score = process_resume(file, job_desc)
    return jsonify({"ranking_score": ranking_score})

if __name__ == "__main__":
    app.run(debug=True)
