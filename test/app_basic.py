import tempfile
import os
from pytube import YouTube
import whisper
# fuck tihs let us transcribe
# but first install - pip install openai-whisper pytube tempfile 

YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


# Transcribe YouTube audio if transcription doesn't exist
if not os.path.exists("transcribe.txt"):
    youtube = YouTube(YOUTUBE_VIDEO)
    audio = youtube.streams.filter(only_audio=True).first()

    # Load the Whisper model
    whisper_model = whisper.load_model("base")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_file = audio.download(output_path=tmpdir)
        transcription = whisper_model.transcribe(audio_file, fp16=False)["text"].strip()

        with open("transcribe.txt", "w") as f:
            f.write(transcription)
