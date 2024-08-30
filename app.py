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

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
PASSCODE = os.getenv("PASSCODE")

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
    # file_extension = files.filename.rsplit('.', 1)[-1]
    # if file_extension != "wav":
    #     abort(415)

    if client_passcode != PASSCODE:
        abort(401)

    whisper_result = WHISPER_MODEL.transcribe(file_path)
    print(whisper_result["text"])
    os.remove(file_path)

    message = client.beta.threads.messages.create(
        thread_id=new_thread.id,
        role="user",
        content=whisper_result["text"]
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
            for msg in messages.data:
                if msg.role == 'assistant':
                    print(msg.content[0].text.value)
                    return msg.content[0].text.value
            break


if __name__ == "__main__":
    APP.run()
