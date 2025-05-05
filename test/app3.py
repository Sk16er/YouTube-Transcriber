import tempfile
import os
from pytubefix import YouTube
import whisper
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Transcribe YouTube audio if transcription doesn't exist
if not os.path.exists("transcribe.txt"):
    try:
        youtube = YouTube(YOUTUBE_VIDEO)
        audio = youtube.streams.filter(only_audio=True).first()
    except Exception as e:
        print(f"Error fetching YouTube video: {e}")
        exit()

    # Load the Whisper model
    whisper_model = whisper.load_model("base")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_file = audio.download(output_path=tmpdir)
        print(f"Audio file path: {audio_file}")  # Debug print
        try:
            transcription = whisper_model.transcribe(audio_file, fp16=False)["text"].strip()
        except Exception as e:
            print(f"Error during transcription: {e}")
            exit()

        with open("transcribe.txt", "w") as f:
            f.write(transcription)