"""
    The main server.

    Lachlan Paul, 2024
"""
import os

import whisper
from flask import Flask, request, abort

APP = Flask(__name__)
WHISPER_MODEL = whisper.load_model("base")
PASSCODE = "p$T9wQz2a#R8fL!sE6hGn5vXyY3jU7iKo0bC1xZ4qJmO"

if not os.path.exists("uploads"):
    os.makedirs("uploads")


@APP.route("/upload", methods=["POST"])
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

    if client_passcode != PASSCODE:
        abort(401)

    result = WHISPER_MODEL.transcribe(files.filename)
    # Delete the file to save space, also because I might get shit if I kept recordings of people talking to a robot.
    os.remove(f"uploads/{files.filename}")

    return result["text"]


if __name__ == "__main__":
    APP.run()
