"""
    File used for testing audio uploads.

    Lachlan Paul, 2024
"""
import os

import requests
from dotenv import load_dotenv


def upload_audio(file_path, server_url):
    load_dotenv()

    with open(file_path, 'rb') as audio_file:
        files = {"audio_file": audio_file}
        headers = {"Passcode": os.getenv("PASSCODE")}

        response = requests.post(server_url, files=files, headers=headers)

        print(response.text)


upload_audio("test.wav", "http://127.0.0.1:5000/upload")
