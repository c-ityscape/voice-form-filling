from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import whisper
import re

app = Flask(__name__)

# Function to preprocess email addresses
def preprocess_email(text):
  return re.sub(r' at (the )?rate ', '@', text, flags=re.IGNORECASE)

# Consider lazy loading or model pooling for scalability
model = None

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

  # Sanitize filename (optional)
  # filename = os.path.splitext(os.path.basename(filename))[0]

  # Save the file to the uploads directory
  os.makedirs("uploads", exist_ok=True)
  file_path = os.path.join("uploads", filename)
  audio_file.save(file_path)

  # Load the Whisper model (consider lazy loading/pooling)
  global model
  if model is None:
    model = whisper.load_model("tiny")

  try:
    result = model.transcribe(file_path)
    transcribed_text = result.get("text", "")

    # Identify the field based on the request data (e.g., using a hidden field)
    field_name = request.form.get('field_id')

    # Preprocess text based on the field
    if field_name == 'email' or field_name == 'loginEmail':
      processed_text = preprocess_email(transcribed_text)
    else:
      processed_text = transcribed_text

    # Debugging print statements
    print(f"Transcribed text: {transcribed_text}")
    print(f"Processed text: {processed_text}")

    # Delete the uploaded file after transcription
    os.remove(file_path)

    return jsonify({"message": "Audio file processed successfully.", "text": processed_text})
  except whisper.DecodingError as e:
    return jsonify({"message": f"Decoding error: {str(e)}"}), 500
  except Exception as e:
    return jsonify({"message": f"Failed to process audio: {str(e)}"}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))