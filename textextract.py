import streamlit as ui
from groq import Groq
import os, tempfile
ui.title("Text Extract")
ui.subheader("text extractor yes")
upload = ui.file_uploader("lol",type=["mp3", "m4a", "ogg", "webm", "wav", "mp4"])
client = Groq(api_key=ui.secrets["groq_api_key"])
def transcribe(path):
    with open(path, "rb") as f:
        transcriber = client.audio.transcriptions.create(
            model = "whisper-large-v3",
            file = (os.path.basename(path), f),
            response_format = "text"
        )
    return transcriber
if upload:
    if upload.size / 1024**2 > 25:
        ui.error("the file that you provided is too big!")
    elif ui.button("Extract", key="file_btn"):
        with ui.spinner("Extracting..."):
            ext = os.path.splitext(upload.name)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(upload.read())
                path = tmp.name
            try:
                transcriber = transcribe(path)
            finally:
                os.unlink(path)
        if not transcribe or len(transcriber.strip()) < 5:
            ui.error("It's Empty")
        else:
            ui.subheader("Extracted text:")
            ui.write(transcriber)
            ui.download_button("download text", transcriber, file_name="extracted_text.txt")