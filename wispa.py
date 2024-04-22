"""
    File used for testing audio uploads.

    Lachlan Paul, 2024
"""
import requests


def upload_audio(file_path, server_url):
    with open(file_path, 'rb') as audio_file:
        files = {"audio_file": audio_file}
        headers = {"Passcode": "p$T9wQz2a#R8fL!sE6hGn5vXyY3jU7iKo0bC1xZ4qJmO"}

        response = requests.post(server_url, files=files, headers=headers)

        print(response.text)


upload_audio("test.wav", "http://127.0.0.1:5000/upload")
