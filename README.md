# Voice-Based Form Filling 

This is a Flask-based web application that leverages OpenAI's Whisper model for transcribing audio input to text. The app facilitates voice-driven form filling by allowing users to upload audio files containing their responses. The application processes the audio files, extracts the transcribed text, and maps it to specific form fields.

**Deployment Link:** [Voice Form Filling App](https://voice-form-filling.onrender.com)

---
## Screenshots
![Screenshot 1](https://github.com/c-ityscape/voice-form-filling/blob/main/Screenshot%202024-12-26%20134247.png)
![Screenshot 2](URL_TO_YOUR_SECOND_IMAGE)

## Features
- **Voice-to-Text Transcription**: Uses OpenAI's Whisper model to transcribe uploaded audio files.
- **Field-Specific Processing**: Automatically processes transcription for specific fields, such as email addresses, replacing phrases like "at the rate" with "@" and "dot" with ".".
- **Simple Web Interface**: Provides a form-based web interface for easy interaction.

---

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

---

## Installation

### 1. Clone the Repository
```bash
https://github.com/yourusername/voice-form-filling.git
cd voice-form-filling
```

### 2. Install Dependencies
Ensure you have all necessary dependencies installed by using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. Download Whisper Model
The application uses the "tiny" version of Whisper. This will be downloaded automatically when you run the app.

---

## Usage

### 1. Run the Application
```bash
python app.py
```

### 2. Access the Application
Open a browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Upload Audio and Fill Forms
- Use the **signup form** at `/` to start.
- If directed to the **registration page**, navigate to `/registration`.
- Upload an audio file corresponding to a form field and view the transcribed text.

---

## Deployment
The application is deployed on platform[Render](https://render.com). However, due to memory constraints on free-tier deployments, the audio upload feature might not work reliably.

**Demo Link:** [Voice Form Filling App](https://voice-form-filling.onrender.com)
(Note: Upload functionality may fail on Render due to memory limitations.)

For local use, run the app manually as described above.

---

## Project Structure
```
voice-form-filling/
|│   app.py                # Main Flask application
|│   requirements.txt     # Dependencies
|├── templates/         # HTML templates for the app
|    |│   signup.html       # Signup form template
|    |│   registration.html # Registration form template
|└── uploads/            # Directory for uploaded audio files (created dynamically)
```

---

## Known Issues
- **Memory Constraints**: Free-tier deployments on platforms like Render may fail to handle large audio files.
- **Static Demo**: The hosted demo does not support file uploads due to deployment limitations.

---

## Credits
- **Whisper Model**: Developed by OpenAI.
- Flask Framework: Lightweight Python web framework.

