# import os
# import math
# import io
# from flask import Flask, request, jsonify, render_template
# import speech_recognition as sr
# from pydub import AudioSegment
# from pydub.utils import which

# # Set up ffmpeg path for pydub
# AudioSegment.converter = which("ffmpeg")

# app = Flask(__name__)

# # Function to handle large audio files and transcription
# def transcribe_large_audio(audio_segment, chunk_length_ms=60000):
#     recognizer = sr.Recognizer()
#     audio_length_ms = len(audio_segment)
#     total_chunks = math.ceil(audio_length_ms / chunk_length_ms)
#     transcriptions = []

#     for i in range(total_chunks):
#         start_time = i * chunk_length_ms
#         end_time = start_time + chunk_length_ms
#         chunk = audio_segment[start_time:end_time]
        
#         # Convert chunk to wav in-memory (no saving to disk)
#         with io.BytesIO() as wav_buffer:
#             chunk.export(wav_buffer, format="wav")
#             wav_buffer.seek(0)

#             with sr.AudioFile(wav_buffer) as source:
#                 audio_data = recognizer.record(source)
#                 try:
#                     text = recognizer.recognize_google(audio_data)
#                     transcriptions.append(text)
#                 except sr.UnknownValueError:
#                     transcriptions.append(f"Chunk {i+1} could not be understood.")
#                 except sr.RequestError:
#                     transcriptions.append(f"Chunk {i+1} had an API error.")

#     return " ".join(transcriptions)

# # # Format the transcription result into readable paragraphs
# # def format_transcription(transcription):
# #     sentences = transcription.split(". ")
# #     formatted_transcription = "<br><br>".join(sentences) + "."  # Add double line break between sentences
# #     return formatted_transcription

# def format_transcription(transcription):
#     # Split the transcription into sentences based on full stops and line breaks
#     sentences = transcription.split('. ')
    
#     # Group sentences into paragraphs (e.g., 3 sentences per paragraph)
#     paragraph_length = 3
#     paragraphs = [" ".join(sentences[i:i + paragraph_length]) for i in range(0, len(sentences), paragraph_length)]
    
#     # Join paragraphs with double line breaks to create readable spacing
#     formatted_transcription = "<br><br>".join(paragraphs) + "."
#     return formatted_transcription



# # Frontend route for file upload page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # API route for file upload and transcription
# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'file' not in request.files:
#         return render_template('index.html', transcription="No file uploaded."), 400

#     file = request.files['file']
    
#     if file.filename == '':
#         return render_template('index.html', transcription="No selected file."), 400

#     # Only process MP3 files
#     if file and file.filename.endswith('.mp3'):
#         try:
#             # Read audio file directly from memory
#             audio = AudioSegment.from_mp3(file)
            
#             # Transcribe large audio using chunks
#             transcription = transcribe_large_audio(audio)

#             # Format transcription for readability
#             formatted_transcription = format_transcription(transcription)

#         except Exception as e:
#             formatted_transcription = f"Error during transcription: {str(e)}"

#         # If the request comes from an API client, return JSON response
#         if request.headers.get('Content-Type') == 'application/json':
#             return jsonify({"transcription": transcription})

#         # Default response to render HTML page with transcription
#         return render_template('index.html', transcription=formatted_transcription)
#     else:
#         return render_template('index.html', transcription="Invalid file format. Only MP3 allowed."), 400

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import math
import io
from flask import Flask, request, jsonify, render_template, send_file
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import pyttsx3
import docx
import PyPDF2

# Set up ffmpeg path for pydub
AudioSegment.converter = which("ffmpeg")

app = Flask(__name__)

# Helper function to handle large audio files and transcription
def transcribe_large_audio(audio_segment, chunk_length_ms=60000):
    recognizer = sr.Recognizer()
    audio_length_ms = len(audio_segment)
    total_chunks = math.ceil(audio_length_ms / chunk_length_ms)
    transcriptions = []

    for i in range(total_chunks):
        start_time = i * chunk_length_ms
        end_time = start_time + chunk_length_ms
        chunk = audio_segment[start_time:end_time]
        
        # Convert chunk to wav in-memory (no saving to disk)
        with io.BytesIO() as wav_buffer:
            chunk.export(wav_buffer, format="wav")
            wav_buffer.seek(0)

            with sr.AudioFile(wav_buffer) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                    transcriptions.append(text)
                except sr.UnknownValueError:
                    transcriptions.append(f"Chunk {i+1} could not be understood.")
                except sr.RequestError:
                    transcriptions.append(f"Chunk {i+1} had an API error.")

    return " ".join(transcriptions)

# Function to format the transcription into readable paragraphs
def format_transcription(transcription):
    sentences = transcription.split('. ')
    paragraph_length = 3
    paragraphs = [" ".join(sentences[i:i + paragraph_length]) for i in range(0, len(sentences), paragraph_length)]
    formatted_transcription = "<br><br>".join(paragraphs) + "."
    return formatted_transcription

# Helper function to convert text to audio using pyttsx3 (offline)
def convert_text_to_audio(text, filename, voice_id, speed):
    engine = pyttsx3.init()
    
    # Set voice based on the user's selection
    voices = engine.getProperty('voices')
    if voice_id < len(voices):
        engine.setProperty('voice', voices[voice_id].id)
    
    # Set speed (words per minute)
    engine.setProperty('rate', speed)

    engine.save_to_file(text, filename)
    engine.runAndWait()

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# Function to extract text from docx
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Frontend route for transcription page
@app.route('/')
def index():
    return render_template('index.html')

# Frontend route for text-to-audio conversion page
# @app.route('/text-to-audio')
# def text_to_audio_page():
#     return render_template('text_to_audio.html')
@app.route('/text-to-audio')
def text_to_audio_page():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return render_template('text_to_audio.html', voices=voices)


# API route for file upload and transcription
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400 if request.is_json else render_template('index.html', transcription="No file uploaded.")

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400 if request.is_json else render_template('index.html', transcription="No selected file.")

    # Only process MP3 files
    if file and file.filename.endswith('.mp3'):
        try:
            # Read audio file directly from memory
            audio = AudioSegment.from_mp3(file)
            
            # Transcribe large audio using chunks
            transcription = transcribe_large_audio(audio)

            # Format transcription for readability
            formatted_transcription = format_transcription(transcription)

        except Exception as e:
            formatted_transcription = f"Error during transcription: {str(e)}"

        # JSON response for API request
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"transcription": transcription})

        # HTML response for normal web request
        return render_template('index.html', transcription=formatted_transcription)

    return jsonify({"error": "Invalid file format. Only MP3 allowed."}), 400 if request.is_json else render_template('index.html', transcription="Invalid file format. Only MP3 allowed.")

# API route for converting text to audio
@app.route('/convert-to-audio', methods=['POST'])
def convert_to_audio():
    if 'textfile' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400 if request.is_json else render_template('text_to_audio.html', error="No file uploaded.")

    file = request.files['textfile']
    
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400 if request.is_json else render_template('text_to_audio.html', error="No selected file.")

    # Extract text based on file type
    if file.filename.endswith('.txt'):
        text = file.read().decode('utf-8')
    elif file.filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    elif file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    else:
        return jsonify({"error": "Invalid file format. Only txt, docx, and pdf allowed."}), 400 if request.is_json else render_template('text_to_audio.html', error="Invalid file format. Only txt, docx, and pdf allowed.")

    # Get user selected options
    voice_id = int(request.form.get('voice', 0))  # Default to first voice
    speed = int(request.form.get('speed', 150))  # Default speed

    # Convert extracted text to audio
    output_filename = "output_audio.mp3"
    convert_text_to_audio(text, output_filename, voice_id, speed)

    # JSON response for API
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({"message": "Text converted to audio", "filename": output_filename})

    # HTML response for web
    return send_file(output_filename, as_attachment=True, download_name=output_filename)

if __name__ == '__main__':
    app.run(debug=True)



# import os
# import math
# import io
# from flask import Flask, request, jsonify, render_template, send_file
# import speech_recognition as sr
# from pydub import AudioSegment
# from pydub.utils import which
# import pyttsx3
# import docx
# import PyPDF2

# # Set up ffmpeg path for pydub
# AudioSegment.converter = which("ffmpeg")

# app = Flask(__name__)

# # Helper function to handle large audio files and transcription
# def transcribe_large_audio(audio_segment, chunk_length_ms=60000):
#     recognizer = sr.Recognizer()
#     audio_length_ms = len(audio_segment)
#     total_chunks = math.ceil(audio_length_ms / chunk_length_ms)
#     transcriptions = []

#     for i in range(total_chunks):
#         start_time = i * chunk_length_ms
#         end_time = start_time + chunk_length_ms
#         chunk = audio_segment[start_time:end_time]
        
#         # Convert chunk to wav in-memory (no saving to disk)
#         with io.BytesIO() as wav_buffer:
#             chunk.export(wav_buffer, format="wav")
#             wav_buffer.seek(0)

#             with sr.AudioFile(wav_buffer) as source:
#                 audio_data = recognizer.record(source)
#                 try:
#                     text = recognizer.recognize_google(audio_data)
#                     transcriptions.append(text)
#                 except sr.UnknownValueError:
#                     transcriptions.append(f"Chunk {i+1} could not be understood.")
#                 except sr.RequestError:
#                     transcriptions.append(f"Chunk {i+1} had an API error.")

#     return " ".join(transcriptions)

# # Function to format the transcription into readable paragraphs
# def format_transcription(transcription):
#     sentences = transcription.split('. ')
#     paragraph_length = 3
#     paragraphs = [" ".join(sentences[i:i + paragraph_length]) for i in range(0, len(sentences), paragraph_length)]
#     formatted_transcription = "<br><br>".join(paragraphs) + "."
#     return formatted_transcription

# # Helper function to convert text to audio using pyttsx3 (offline)
# def convert_text_to_audio(text, filename):
#     engine = pyttsx3.init()
#     engine.save_to_file(text, filename)
#     engine.runAndWait()

# # Function to extract text from PDF
# def extract_text_from_pdf(file):
#     reader = PyPDF2.PdfReader(file)
#     text = ""
#     for page_num in range(len(reader.pages)):
#         text += reader.pages[page_num].extract_text()
#     return text

# # Function to extract text from docx
# def extract_text_from_docx(file):
#     doc = docx.Document(file)
#     return "\n".join([para.text for para in doc.paragraphs])

# # Frontend route for transcription page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Frontend route for text-to-audio conversion page
# @app.route('/text-to-audio')
# def text_to_audio_page():
#     return render_template('text_to_audio.html')

# # API route for file upload and transcription
# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded."}), 400 if request.is_json else render_template('index.html', transcription="No file uploaded.")

#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({"error": "No selected file."}), 400 if request.is_json else render_template('index.html', transcription="No selected file.")

#     # Only process MP3 files
#     if file and file.filename.endswith('.mp3'):
#         try:
#             # Read audio file directly from memory
#             audio = AudioSegment.from_mp3(file)
            
#             # Transcribe large audio using chunks
#             transcription = transcribe_large_audio(audio)

#             # Format transcription for readability
#             formatted_transcription = format_transcription(transcription)

#         except Exception as e:
#             formatted_transcription = f"Error during transcription: {str(e)}"

#         # JSON response for API request
#         if request.headers.get('Content-Type') == 'application/json':
#             return jsonify({"transcription": transcription})

#         # HTML response for normal web request
#         return render_template('index.html', transcription=formatted_transcription)

#     return jsonify({"error": "Invalid file format. Only MP3 allowed."}), 400 if request.is_json else render_template('index.html', transcription="Invalid file format. Only MP3 allowed.")

# # API route for converting text to audio
# @app.route('/convert-to-audio', methods=['POST'])
# def convert_to_audio():
#     if 'textfile' not in request.files:
#         return jsonify({"error": "No file uploaded."}), 400 if request.is_json else render_template('text_to_audio.html', error="No file uploaded.")

#     file = request.files['textfile']
    
#     if file.filename == '':
#         return jsonify({"error": "No selected file."}), 400 if request.is_json else render_template('text_to_audio.html', error="No selected file.")

#     # Extract text based on file type
#     if file.filename.endswith('.txt'):
#         text = file.read().decode('utf-8')
#     elif file.filename.endswith('.docx'):
#         text = extract_text_from_docx(file)
#     elif file.filename.endswith('.pdf'):
#         text = extract_text_from_pdf(file)
#     else:
#         return jsonify({"error": "Invalid file format. Only txt, docx, and pdf allowed."}), 400 if request.is_json else render_template('text_to_audio.html', error="Invalid file format. Only txt, docx, and pdf allowed.")

#     # Convert extracted text to audio
#     output_filename = "output_audio.mp3"
#     convert_text_to_audio(text, output_filename)

#     # JSON response for API
#     if request.headers.get('Content-Type') == 'application/json':
#         return jsonify({"message": "Text converted to audio", "filename": output_filename})

#     # HTML response for web
#     return send_file(output_filename, as_attachment=True, download_name=output_filename)

# if __name__ == '__main__':
#     app.run(debug=True)
