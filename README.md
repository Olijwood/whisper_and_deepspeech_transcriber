This is a transcriber that returns a transcription by WhisperAI and DeepSpeech (Mozilla) to the user. If you run app.py you will be able to go to: https://127.0.0.0/5000 where you will see the file uploader. It is compatible with: '.wav', '.mp3' and '.mp4' audio files. This transcriber uses Ray to run the two transcription functions simultaneously.

To get this transcriber up and running you will need to download the deepspeech model's '.ppbm' & '.scorer' file from this link:
https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3

You then need to move these files into a folder called 'models' in this directory.
You will also need the python libraries:
DeepSpeech,
Whisper,
PyDub,
Flask,
Flask-cors,
webrtcvad,
Contextlib,
Moviepy,
Ray

Once you've uploaded the audio file, after a few minutes you should see the Whisper Transcription on the left and the DeepSpeech Transcription on the right. This works with longer audio_files such as podcasts too.
