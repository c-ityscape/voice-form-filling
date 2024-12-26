from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import whisper
import re
from werkzeug.utils import secure_filename
import gc  # For garbage collection

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm', 'ogg'}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model only when needed
model = None

def get_model():
    global model
    if model is None:
        model = whisper.load_model("base.en")
    return model

def cleanup_model():
    global model
    if model is not None:
        del model
        model = None
        gc.collect()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_email(text):
    text = text.lower()
    text = re.sub(r'\s+at\s+(?:the\s+)?rate\s+', '@', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+dot\s+', '.', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', '', text)
    return text

@app.route('/')
def home():
    return redirect(url_for('server_signup'))

@app.route('/signup')
def server_signup():
    return render_template('signup.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return jsonify({"message": "No audio file provided"}), 400

    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not allowed_file(audio_file.filename):
        return jsonify({"message": "File type not allowed"}), 400

    try:
        # Secure the filename and save file
        filename = secure_filename(audio_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(file_path)

        # Load model only when needed
        model = get_model()

        # Process with Whisper
        result = model.transcribe(
            file_path,
            fp16=False,  # Force FP32 on CPU
            language='en'
        )

        transcribed_text = result.get("text", "")

        # Process based on context
        context = request.form.get("context", "").lower()
        if context in ['email', 'loginemail']:
            transcribed_text = preprocess_email(transcribed_text)

        # Clean up
        cleanup_model()
        
        return jsonify({
            "message": "Audio file processed successfully.",
            "text": transcribed_text
        }), 200

    except Exception as e:
        cleanup_model()
        return jsonify({"message": f"Failed to process audio: {str(e)}"}), 500

    finally:
        # Clean up the file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing temporary file: {e}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)