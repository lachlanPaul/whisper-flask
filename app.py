"""
    The main server.

    Lachlan Paul, 2024
"""
import os

import whisper
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, abort

APP = Flask(__name__)
WHISPER_MODEL = whisper.load_model("base")
PASSCODE = "p$T9wQz2a#R8fL!sE6hGn5vXyY3jU7iKo0bC1xZ4qJmO"

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)

assistant = client.beta.assistants.create(
  name="Pepper Robot",
  instructions="You are the Pepper Robot produced by SoftBank Robotics. You are polite, bubbly, and ready to help in any way you can",
  model="gpt-3.5-turbo",
)

new_thread = client.beta.threads.create()

if not os.path.exists("uploads"):
    os.makedirs("uploads")


@APP.route("/upload", methods=["POST"])
def upload_file():
    files = request.files["audio_file"]
    file_path = f"uploads/{files.filename}"
    files.save(file_path)
    client_passcode = request.headers.get("Passcode")

    # Checks to make sure file is only a wav.
    # While other file types could be used, we're going to just stick to using wav files.
    # Why? ¯\_(ツ)_/¯
    file_extension = files.filename.rsplit('.', 1)[-1]
    if file_extension != "wav":
        abort(415)

    if client_passcode != PASSCODE:
        abort(401)

    # Transcribe the saved file instead of the file object
    with open(file_path, 'rb') as audio_file:
        whisper_result = WHISPER_MODEL.transcribe(audio_file)
    os.remove(file_path)

    message = client.beta.threads.messages.create(
        thread_id=new_thread.id,
        role="user",
        content=whisper_result
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=new_thread.id,
        assistant_id=assistant.id
    )

    while True:
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=new_thread.id
            )
            print(messages[-1])


if __name__ == "__main__":
    APP.run()
