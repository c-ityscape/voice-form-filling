from flask import Flask, request, jsonify, send_from_directory, render_template,redirect,url_for
import os
import whisper
import re

app = Flask(__name__)
model=whisper.load_model("small.en")
# Function to preprocess email addresses
def preprocess_email(text):

  return re.sub(r' at (the )?rate ', '@', text, flags=re.IGNORECASE)

# Consider lazy loading or model pooling for scalability

@app.route('/')
def home():
  return redirect(url_for('server_signup'))  # Serve signup form FIRST
@app.route('/signup') #New route for signup page
def server_signup():
  return render_template('signup.html')

@app.route('/registration') #New route for registration page
def registration():
  return render_template('registration.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
  if 'audio_file' not in request.files:
    return jsonify({"message": "No audio file provided"}), 400

  audio_file = request.files['audio_file']
  context=request.form.get("context","").lower()
  filename=audio_file.filename

  # Sanitize filename (optional)
  # filename = os.path.splitext(os.path.basename(filename))[0]

  # Save the file to the uploads directory
  os.makedirs("uploads", exist_ok=True)
  file_path = os.path.join("uploads", filename)
  audio_file.save(file_path)

  try:
    result = model.transcribe(file_path)
    transcribed_text = result.get("text", "")
    print(context)
    # Preprocess text based on the field
    if context == 'email' or context == 'loginEmail':
      transcribed_text = preprocess_email(transcribed_text)

    os.remove(file_path)
    return jsonify({"message": "Audio file processed successfully.", "text": transcribed_text}), 200

  except Exception as e:
    return jsonify({"message": f"Failed to process audio: {str(e)}"}), 500
def preprocess_email(transcription):
    transcription = transcription.lower()
    transcription = transcription.replace(" at ", "@")
    transcription = transcription.replace(" dot ", ".")
    transcription = transcription.replace(" ", "")
    return transcription
if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port,debug=True)