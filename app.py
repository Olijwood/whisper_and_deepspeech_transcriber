from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import whisper_transcriber
import whisper_audio_formatter
import time
import deepspeech_transcriber
import ray

app = Flask(__name__)
CORS(app)

APP__ROOT = os.path.dirname(os.path.abspath(__name__))


@app.route("/", methods=["GET", "POST"])
def get_message():
    if request.method == "GET":
        print("Got request in main function")
        return render_template("index.html")


@app.route("/upload_static_file", methods=["GET", "POST"])
def upload_static_file():
    print("Got request in static files")

    target = os.path.join(APP__ROOT, "unformatted_audio/")

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("static_file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    time.sleep(1)
    whisper_audio_formatter.audioFormatter()
    
    dir_path = os.getcwd()

    ray.init()

    @ray.remote
    def whisper_t():
        whisper_transcriber.main()
        whisper_transcription_path = f"{dir_path}/whisper_transcription/"
        for item in os.listdir(whisper_transcription_path):
            if item.endswith('.txt'):
                with open(str(whisper_transcription_path + item), "r") as f:
                    whisper_text = f.read()
        return whisper_text

    @ray.remote
    def deepspeech_t():
        deepspeech_transcriber.main()
        deepspeech_transcription_path = f'{dir_path}/deepspeech_transcription/'
        for item in os.listdir(deepspeech_transcription_path):
            if item.endswith('.txt'):
                with open(str(deepspeech_transcription_path + item), 'r') as g:
                    deepspeech_text = g.read()
        return deepspeech_text

    run_both = [whisper_t.remote(), deepspeech_t.remote()]
    ray.get(run_both)

    deepspeech_transcription_path = f'{dir_path}/deepspeech_transcription/'
    for item in os.listdir(deepspeech_transcription_path):
            if item.endswith('.txt'):
                with open(str(deepspeech_transcription_path + item), 'r') as g:
                    deepspeech_text = g.read()
    whisper_transcription_path = f"{dir_path}/whisper_transcription/"
    for item in os.listdir(whisper_transcription_path):
        if item.endswith('.txt'):
            with open(str(whisper_transcription_path + item), "r") as f:
                whisper_text = f.read()
    resp = {'success': True, 'whisper_transcription': whisper_text, 'deepspeech_transcription': deepspeech_text}

    return jsonify(resp), 200  # 1:58.97


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
