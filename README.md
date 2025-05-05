YouTube Transcriber
   🎙️ YouTube Transcriber 🎙️
   -------------------------
   Transcribe YouTube videos with ease!

Overview
YouTube Transcriber is a Python-based tool that allows you to download audio from YouTube videos and transcribe it into text using the whisper model by OpenAI. This project is designed to be robust, user-friendly, and future-proof, with features like:

Input YouTube URLs via command line (no hardcoding).
Automatic transcription with sentence formatting.
Save transcriptions with video titles as filenames.
Loop to transcribe multiple videos.
Fallback mechanisms for audio download (pytubefix and yt-dlp).
Option to manually provide an audio file for transcription.
Detailed error handling and logging for debugging.

This tool is perfect for anyone who wants to transcribe YouTube videos for notes, subtitles, or content analysis.
Features

Dynamic URL Input: Enter YouTube URLs at runtime via command line.
Automatic Transcription: Uses whisper to transcribe audio with high accuracy.
Sentence Formatting: Transcription is formatted into readable sentences using nltk.
Video Title as Filename: Transcriptions are saved with the video title (e.g., Katy_Perry_-_Harleys_In_Hawaii_(Official).txt).
Loop for Multiple Videos: Transcribe multiple videos in one session.
Fallback Audio Download: Uses pytubefix for downloading audio, with yt-dlp as a fallback if pytubefix fails.
Manual Audio Input: Option to provide a local audio file for transcription if YouTube download fails.
Error Handling: Robust error handling with detailed logs to help debug issues.
Future-Proof Design: Includes strategies to handle YouTube API changes and library updates.

Prerequisites
Before running the tool, ensure you have the following installed:
Software Requirements

Python 3.7 or higher: Download from python.org.
FFmpeg: Required for audio processing by whisper.

Python Dependencies

pytubefix: For downloading YouTube audio.
yt-dlp: Fallback library for downloading YouTube audio.
openai-whisper: For audio transcription.
nltk: For sentence segmentation in transcriptions.

Installation
Follow these steps to set up the project:
1. Clone the Repository
If you haven't already created a repository, you can initialize one and add this project:
git init
git add .
git commit -m "Initial commit: YouTube Transcriber"

2. Install Python Dependencies
Install the required Python packages using pip:
pip install pytubefix yt-dlp openai-whisper nltk

3. Install FFmpeg
FFmpeg is required for whisper to process audio files. Install it using one of the following methods:
On Windows (using winget):
winget install ffmpeg

On Windows (Manual Installation):

Download FFmpeg from FFmpeg Builds.
Extract the zip file to a folder (e.g., C:\ffmpeg).
Add C:\ffmpeg\bin to your system Path:
Right-click on This PC > Properties > Advanced system settings > Environment Variables.
Edit Path and add C:\ffmpeg\bin.


Verify installation:ffmpeg -version



On macOS (using brew):
brew install ffmpeg

On Linux (using apt):
sudo apt update
sudo apt install ffmpeg

4. Download NLTK Data
nltk requires the punkt tokenizer for sentence segmentation. Download it by running this Python script:
import nltk
nltk.download('punkt')

Usage
1. Save the Code
Save the main script as youtube_transcriber.py in your project directory. The script is provided in the repository (or you can copy it from the documentation).
2. Run the Script
Run the script using Python:
python youtube_transcriber.py

3. Follow the Prompts

Enter a YouTube URL: Provide a valid YouTube URL (e.g., https://www.youtube.com/watch?v=sQEgklEwhSo).
Or Use Manual Mode: Type manual to provide a local audio file path (e.g., C:/downloads/audio.mp3).
Or Exit: Type exit to quit the program.
Transcribe Multiple Videos: After each transcription, the script will ask if you want to transcribe another video (y/n).

Example Run
Enter YouTube video URL, or type 'manual' to provide an audio file path, or 'exit' to quit:
https://www.youtube.com/watch?v=sQEgklEwhSo
2025-05-05 20:00:00 - DEBUG - Audio downloaded with pytubefix to: C:\Users\shush\AppData\Local\Temp\tmp12345\Katy_Perry_-_Harleys_In_Hawaii_(Official).m4a
Transcription saved to Katy_Perry_-_Harleys_In_Hawaii_(Official).txt
Do you want to transcribe another video? (y/n): y
Enter YouTube video URL, or type 'manual' to provide an audio file path, or 'exit' to quit:
manual
Enter path to audio file (e.g., C:/path/to/audio.mp3): C:/downloads/my_audio.mp3
Enter a title for this audio (for saving transcription): My Audio
Transcription saved to My_Audio.txt
Do you want to transcribe another video? (y/n): n
Exiting program.

Example Transcription File
The transcription will be saved with the video title as the filename. For example, Katy_Perry_-_Harleys_In_Hawaii_(Official).txt might look like:
Oh-oh-oh, oh-oh-oh.
Riding down the coast, yeah.
Harleys in Hawaii, yeah.
...

Code Structure
The main script (youtube_transcriber.py) is organized into modular functions for clarity and maintainability:

clean_filename(title): Cleans the video title to make it a valid filename by replacing special characters.
get_valid_youtube_url(): Prompts the user for a YouTube URL or manual audio file path, with validation.
download_with_pytubefix(youtube_url, tmpdir): Downloads audio using pytubefix.
download_with_ytdlp(youtube_url, tmpdir): Fallback function to download audio using yt-dlp if pytubefix fails.
process_youtube_video(youtube_url): Manages the download and transcription process for YouTube videos.
transcribe_audio(audio_file): Transcribes an audio file using whisper.
format_transcription(transcription): Formats the transcription into readable sentences using nltk.
save_transcription(transcription, video_title): Saves the transcription to a file.
main(): Orchestrates the entire process in a loop.

Troubleshooting
Common Issues and Fixes

Error: No such file or directory for audio file:

Cause: The temporary audio file might be deleted before transcription.
Fix: The script ensures download and transcription happen in the same tempfile.TemporaryDirectory context. Check logs for the file path and ensure it exists.


Error: pytubefix failed or yt-dlp failed:

Cause: YouTube might have changed its API, or there's a rate-limiting issue.
Fix:
Update dependencies:pip install --upgrade pytubefix yt-dlp


Use the manual option to provide a local audio file.
Check pytubefix or yt-dlp GitHub for reported issues:
Pytubefix GitHub
yt-dlp GitHub






Error: ffmpeg not found:

Cause: FFmpeg is not installed or not in the system Path.
Fix:
Verify FFmpeg installation:ffmpeg -version


Ensure ffmpeg is in your Path (see Installation section).




Transcription in One Line:

Cause: nltk sentence segmentation might have failed.
Fix:
Ensure nltk data is downloaded:import nltk
nltk.download('punkt')


The script includes a fallback to split by periods if nltk fails.




General Errors:

Check the logs (they include timestamps and debug messages).
Share the error message and logs with the developer for assistance.



Future-Proofing
YouTube frequently updates its API, which can break audio download libraries like pytubefix or yt-dlp. Here's how to keep this tool working in the future:

Regularly Update Dependencies:Update all dependencies every 1-2 months:
pip install --upgrade pytubefix yt-dlp openai-whisper nltk
winget upgrade ffmpeg


Monitor Library Issues:

Check for updates or issues on the GitHub pages of pytubefix and yt-dlp:
Pytubefix GitHub
yt-dlp GitHub




Manual Audio Download:If both pytubefix and yt-dlp fail, download the audio manually using yt-dlp on the command line:
yt-dlp -x --audio-format m4a -o "audio.m4a" "https://www.youtube.com/watch?v=sQEgklEwhSo"

Then use the manual option in the script to transcribe the audio file.

Alternative Transcription Tools:If whisper stops working, consider alternatives like:

Google Speech-to-Text API
DeepSpeech



Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Some ideas for contributions:

Add support for other transcription models.
Improve sentence segmentation for better formatting.
Add a GUI interface for easier usage.

License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the license terms.
Acknowledgments

Thanks to the developers of pytubefix, yt-dlp, openai-whisper, and nltk for their amazing libraries.
Built with ❤️ for users who need an easy way to transcribe YouTube videos.


Happy Transcribing! 🎙️
