from flask import Flask, request, jsonify, render_template
import os
import whisper
from werkzeug.utils import secure_filename
import io
import numpy as np
import soundfile as sf

app = Flask(__name__)

model = whisper.load_model("tiny")

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return jsonify({"message": "No audio file provided"}), 400

    audio_file = request.files['audio_file']
    filename = secure_filename(audio_file.filename)

    try:
        audio_data = audio_file.stream.read()  # Read the entire stream into memory
        audio_np, sr = sf.read(io.BytesIO(audio_data)) #Convert to numpy array


        result = model.transcribe(audio_data)
        transcribed_text = result.get("text", "")

        field_name = request.form.get('field_id')
        print(field_name)

        if field_name == 'email' or field_name == 'loginEmail':
            transcribed_text = transcribed_text.replace(" at the rate ", "@")
            transcribed_text = transcribed_text.replace(" at rate ", "@")
            transcribed_text = transcribed_text.replace(" at-rate ", "@")
            transcribed_text = transcribed_text.replace(" dot ", ".")
            transcribed_text = transcribed_text.replace(" . ", ".")
            processed_text = transcribed_text
        else:
            processed_text = transcribed_text

        print(f"Transcribed text: {transcribed_text}")
        print(f"Processed text: {processed_text}")

        return jsonify({"message": "Audio file processed successfully.", "text": processed_text}) #Return the processed text

    except Exception as e:
        return jsonify({"message": f"Failed to process audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))