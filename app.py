from flask import Flask, request, jsonify, send_from_directory
import os
import whisper

app = Flask(__name__)

# Load the Whisper model once to reuse for multiple requests
model = whisper.load_model("base")

@app.route('/')
def home():
    
    return send_from_directory('.', 'index.html')  # Serves the index.html file

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return jsonify({"message": "No audio file provided"}), 400

    audio_file = request.files['audio_file']
    filename = audio_file.filename

    # Save the file to the uploads directory
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", filename)
    audio_file.save(file_path)

    # Transcribe the audio using Whisper
    try:
        result = model.transcribe(file_path)
        transcribed_text = result.get("text", "")

        # Delete the uploaded file after transcription to save space
        os.remove(file_path)

        return jsonify({"message": "Audio file processed successfully.", "text": transcribed_text})
    except Exception as e:
        return jsonify({"message": f"Failed to process audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
