from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import os
import uuid

from database import save_result
from forensic.metadata import metadata_check
from forensic.video_analysis import video_check
from forensic.audio_analysis import audio_check


app = Flask(__name__)


# =========================
# KONFIGURASI PATH
# =========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Maksimal upload 500 MB
app.config["MAX_CONTENT_LENGTH"] = (
    500 * 1024 * 1024
)


# Folder otomatis dibuat kalau belum ada
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


ALLOWED_VIDEO = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv"
}


ALLOWED_AUDIO = {
    ".wav",
    ".mp3",
    ".flac",
    ".m4a"
}


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================
# ANALYZE
# =========================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # Pastikan file dikirim
    if "file" not in request.files:

        return (
            "File tidak ditemukan.",
            400
        )


    file = request.files["file"]


    if file.filename == "":

        return (
            "Silakan pilih file.",
            400
        )


    # =========================
    # SIMPAN NAMA ASLI
    # =========================

    original_filename = (
        file.filename
    )


    # Ambil ekstensi
    extension = os.path.splitext(
        original_filename
    )[1].lower()


    # Validasi format
    if (
        extension not in ALLOWED_VIDEO
        and
        extension not in ALLOWED_AUDIO
    ):

        return (
            "Format file tidak didukung.",
            400
        )


    # =========================
    # BUAT NAMA FILE AMAN
    # =========================

    original_base = os.path.splitext(
        original_filename
    )[0]


    safe_base = secure_filename(
        original_base
    )


    # Batasi panjang nama file
    safe_base = safe_base[:60]


    if not safe_base:

        safe_base = "evidence"


    unique_id = uuid.uuid4().hex[:10]


    stored_filename = (
        f"{unique_id}_"
        f"{safe_base}"
        f"{extension}"
    )


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        stored_filename
    )


    # =========================
    # SIMPAN FILE
    # =========================

    file.save(
        filepath
    )


    # =========================
    # ANALISIS
    # =========================

    result = {}


    try:

        result["metadata"] = (
            metadata_check(
                filepath
            )
        )


        if extension in ALLOWED_VIDEO:

            result["analysis"] = (
                video_check(
                    filepath
                )
            )


        elif extension in ALLOWED_AUDIO:

            result["analysis"] = (
                audio_check(
                    filepath
                )
            )


    except Exception as error:

        return (
            f"Terjadi error saat analisis: "
            f"{str(error)}",
            500
        )


    # =========================
    # DATABASE
    # =========================

    save_result(
        original_filename,
        result
    )


    # =========================
    # HASIL
    # =========================

    from flask import jsonify
    return jsonify({
        "filename": original_filename,
        "data": result
    })


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )