import tempfile
import os
import logging
import re
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
    """Prompt user for a valid YouTube URL."""
    while True:
        url = input("Enter YouTube video URL: ").strip()
        if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/"):
            return url
        print("Invalid YouTube URL! Please enter a valid URL (e.g., https://www.youtube.com/watch?v=...)")

def process_youtube_video(youtube_url):
    """Download and transcribe YouTube video."""
    try:
        # Initialize YouTube object
        youtube = YouTube(youtube_url)
        audio_stream = youtube.streams.filter(only_audio=True).first()
        video_title = clean_filename(youtube.title)  # Clean title for filename

        # Create temp directory and process audio
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download audio with cleaned filename
            audio_filename = f"{video_title}.m4a"
            audio_file = os.path.join(tmpdir, audio_filename)
            audio_stream.download(output_path=tmpdir, filename=audio_filename)
            logging.debug(f"Audio downloaded to: {audio_file}")

            # Verify file exists
            if not os.path.exists(audio_file):
                print(f"Error: Audio file {audio_file} not found after download.")
                return None, None

            # Load Whisper model and transcribe
            whisper_model = whisper.load_model("base")
            transcription = whisper_model.transcribe(audio_file, fp16=False)["text"].strip()
            return transcription, video_title

    except Exception as e:
        print(f"Error processing YouTube video: {e}")
        return None, None

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
        # Get YouTube URL
        youtube_url = get_valid_youtube_url()

        # Process video
        transcription, video_title = process_youtube_video(youtube_url)
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