"""Lachlan Paul, 2024"""
import os

import whisper
from flask import Flask, request, abort

app = Flask(__name__)
model = whisper.load_model("base")
passcode = "p$T9wQz2a#R8fL!sE6hGn5vXyY3jU7iKo0bC1xZ4qJmO"

if not os.path.exists("uploads"):
    os.makedirs("uploads")


@app.route("/upload", methods=["POST"])
def upload_file():
    files = request.files["audio_file"]
    files.save(f"uploads/{files.filename}")
    client_passcode = request.headers.get("Passcode")

    # Checks to make sure file is only a wav.
    # While other file types could be used, we're going to just stick to using wav files.
    # Why? Dunno.
    file_extension = files.filename.rsplit('.', 1)[-1]
    if file_extension != "wav":
        abort(415)

    if client_passcode != passcode:
        abort(401)

    result = model.transcribe(files.filename)
    os.remove(f"uploads/{files.filename}")

    return result["text"]


if __name__ == "__main__":
    app.run()
