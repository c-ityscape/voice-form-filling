from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import whisper
import re
app = Flask(__name__)

# Load the Whisper model once to reuse for multiple requests
model = whisper.load_model("base.en" )

@app.route('/')
def home():
    return render_template('signup.html')  # Serve signup form FIRST

@app.route('/registration') #New route for registration page
def registration():
    return render_template('registration.html')

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

        # Identify the field based on the request data (e.g., using a hidden field)
        field_name = request.form.get('field_id') 
        print(field_name)

        # Preprocess the transcribed text based on the field
        if field_name == 'email' or field_name == 'loginEmail':
            transcribed_text = transcribed_text.replace(" at the rate ", "@") 
            transcribed_text = transcribed_text.replace(" at rate ", "@") 
            transcribed_text = transcribed_text.replace(" at-rate ", "@") 
            transcribed_text = transcribed_text.replace(" dot ", ".")
            transcribed_text = transcribed_text.replace(" . ", ".") 
           
            processed_text = transcribed_text
        else:
            processed_text = transcribed_text

        # Debugging print statement
        print(f"Transcribed text: {transcribed_text}")
        print(f"Processed text: {processed_text}") 

        # Delete the uploaded file after transcription to save space
        os.remove(file_path)

        return jsonify({"message": "Audio file processed successfully.", "text": transcribed_text})
    except Exception as e:
        return jsonify({"message": f"Failed to process audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)