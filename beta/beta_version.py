# pip install --upgrade pytubefix
#pip install --upgrade openai-whisper
# winget upgrade ffmpeg
# pip install yt-dlp
# every time you run this script, it will download the latest version of ffmpeg and pytubefix in case of the venv
# pip install --upgrade pytubefix yt-dlp openai-whisper nltk
# winget upgrade ffmpeg
# pip install --upgrade pytubefix yt-dlp
import tempfile
import os
import logging
import re
import subprocess
from pytubefix import YouTube
import whisper
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK punkt tokenizer for sentence segmentation (run once)
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"Error downloading NLTK punkt: {e}")
    exit()

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_filename(title):
    """Clean video title to make it a valid filename."""
    # Replace invalid characters and special characters
    cleaned = re.sub(r'[\/:*?"<>|]', '_', title)
    cleaned = re.sub(r'[.…]', '_', cleaned)  # Handle ellipsis and dots
    return cleaned.strip()

def get_valid_youtube_url():
    """Prompt user for a valid YouTube URL or audio file path."""
    while True:
        print("Enter YouTube video URL, or type 'manual' to provide an audio file path, or 'exit' to quit:")
        user_input = input().strip()
        if user_input.lower() == 'exit':
            return None
        if user_input.lower() == 'manual':
            audio_path = input("Enter path to audio file (e.g., C:/path/to/audio.mp3): ").strip()
            if os.path.exists(audio_path):
                video_title = input("Enter a title for this audio (for saving transcription): ").strip()
                return audio_path, clean_filename(video_title), True
            print("Invalid audio file path! Please try again.")
            continue
        if user_input.startswith("https://www.youtube.com/watch?v=") or user_input.startswith("https://youtu.be/"):
            return user_input, None, False
        print("Invalid YouTube URL! Please enter a valid URL (e.g., https://www.youtube.com/watch?v=...)")

def download_with_pytubefix(youtube_url, tmpdir):
    """Download audio using pytubefix."""
    try:
        youtube = YouTube(youtube_url)
        audio_stream = youtube.streams.filter(only_audio=True).first()
        video_title = clean_filename(youtube.title)
        audio_filename = f"{video_title}.m4a"
        audio_file = os.path.join(tmpdir, audio_filename)
        audio_stream.download(output_path=tmpdir, filename=audio_filename)
        logging.debug(f"Audio downloaded with pytubefix to: {audio_file}")
        return audio_file, video_title
    except Exception as e:
        logging.error(f"pytubefix failed: {e}")
        return None, None

def download_with_ytdlp(youtube_url, tmpdir):
    """Fallback: Download audio using yt-dlp."""
    try:
        youtube = YouTube(youtube_url)
        video_title = clean_filename(youtube.title)
        audio_filename = f"{video_title}.m4a"
        audio_file = os.path.join(tmpdir, audio_filename)
        cmd = [
            'yt-dlp',
            '-x',  # Extract audio
            '--audio-format', 'm4a',
            '-o', audio_file,
            youtube_url
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.debug(f"Audio downloaded with yt-dlp to: {audio_file}")
        return audio_file, video_title
    except Exception as e:
        logging.error(f"yt-dlp failed: {e}")
        return None, None

def process_youtube_video(youtube_url):
    """Download and transcribe YouTube video."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Try pytubefix first
        audio_file, video_title = download_with_pytubefix(youtube_url, tmpdir)
        if audio_file and os.path.exists(audio_file):
            return transcribe_audio(audio_file), video_title

        # Fallback to yt-dlp
        print("pytubefix failed, trying yt-dlp...")
        audio_file, video_title = download_with_ytdlp(youtube_url, tmpdir)
        if audio_file and os.path.exists(audio_file):
            return transcribe_audio(audio_file), video_title

        print("Error: Could not download audio with pytubefix or yt-dlp.")
        return None, None

def transcribe_audio(audio_file):
    """Transcribe audio file using Whisper model."""
    try:
        whisper_model = whisper.load_model("base")
        transcription = whisper_model.transcribe(audio_file, fp16=False)["text"].strip()
        return transcription
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def format_transcription(transcription):
    """Format transcription into readable sentences."""
    try:
        sentences = sent_tokenize(transcription)
        return "\n".join(sentences)
    except Exception as e:
        print(f"Error formatting transcription: {e}")
        # Fallback: Split by periods if NLTK fails
        return "\n".join(transcription.split('. '))

def save_transcription(transcription, video_title):
    """Save transcription to a file named after the video title."""
    try:
        filename = f"{video_title}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcription)
        print(f"Transcription saved to {filename}")
    except Exception as e:
        print(f"Error saving transcription: {e}")

def main():
    """Main function to run the transcription process in a loop."""
    while True:
        # Get YouTube URL or audio file path
        result = get_valid_youtube_url()
        if result is None:
            print("Exiting program.")
            break
        user_input, video_title, is_manual = result

        # Process based on input type
        if is_manual:
            transcription = transcribe_audio(user_input)
        else:
            transcription, video_title = process_youtube_video(user_input)

        if not transcription or not video_title:
            print("Skipping due to error in processing.")
            continue

        # Format and save transcription
        formatted_transcription = format_transcription(transcription)
        save_transcription(formatted_transcription, video_title)

        # Ask to continue or exit
        choice = input("Do you want to transcribe another video? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()