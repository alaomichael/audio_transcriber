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
# import requests
# import zipfile

# def download_ffmpeg_former():
#     ffmpeg_url = "https://drive.google.com/file/d/1gKl_HiRnh8nKOrfm1FQyhHPoANA8GumK/view?usp=sharing"
#     ffmpeg_zip_path = "ffmpeg.zip"

#     # Download the zip file
#     response = requests.get(ffmpeg_url)
#     with open(ffmpeg_zip_path, "wb") as f:
#         f.write(response.content)

#     # Extract the zip file
#     with zipfile.ZipFile(ffmpeg_zip_path, 'r') as zip_ref:
#         zip_ref.extractall("ffmpeg_binaries")

#     # Remove the zip file
#     os.remove(ffmpeg_zip_path)

#     # Set executable permission if on Linux/macOS
#     if os.name != 'nt':  # If not Windows
#         os.chmod("ffmpeg_binaries/ffmpeg", 0o755)

# def download_ffmpeg():
#     file_id = '1gKl_HiRnh8nKOrfm1FQyhHPoANA8GumK'  # Replace with your file ID
#     url = f"https://drive.google.com/uc?export=download&id={file_id}"
#     ffmpeg_zip_path = "ffmpeg.zip"

#     response = requests.get(url)
#     with open(ffmpeg_zip_path, "wb") as f:
#         f.write(response.content)

#     # Extract the zip file
#     with zipfile.ZipFile(ffmpeg_zip_path, 'r') as zip_ref:
#         zip_ref.extractall("ffmpeg_binaries")

#     os.remove(ffmpeg_zip_path)
#     if os.name != 'nt':
#         os.chmod("ffmpeg_binaries/ffmpeg", 0o755)


# # Call the function during startup
# download_ffmpeg()
# # # Set up ffmpeg path for pydub
# # AudioSegment.converter = which("ffmpeg")

# # Set the path to the ffmpeg binary
# # Update this path to match your project structure
# # ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg_binaries", "ffmpeg")

# # For Windows, ensure the binary is named `ffmpeg.exe`
# ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg_binaries", "ffmpeg.exe")

# # Tell pydub to use the local ffmpeg binary
# AudioSegment.converter = ffmpeg_path

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
# def convert_text_to_audio(text, filename, voice_id, speed):
#     engine = pyttsx3.init()
    
#     # Set voice based on the user's selection
#     voices = engine.getProperty('voices')
#     if voice_id < len(voices):
#         engine.setProperty('voice', voices[voice_id].id)
    
#     # Set speed (words per minute)
#     engine.setProperty('rate', speed)

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
# # @app.route('/text-to-audio')
# # def text_to_audio_page():
# #     return render_template('text_to_audio.html')
# @app.route('/text-to-audio')
# def text_to_audio_page():
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     return render_template('text_to_audio.html', voices=voices)


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

#     # Get user selected options
#     voice_id = int(request.form.get('voice', 0))  # Default to first voice
#     speed = int(request.form.get('speed', 150))  # Default speed

#     # Convert extracted text to audio
#     output_filename = "output_audio.mp3"
#     convert_text_to_audio(text, output_filename, voice_id, speed)

#     # JSON response for API
#     if request.headers.get('Content-Type') == 'application/json':
#         return jsonify({"message": "Text converted to audio", "filename": output_filename})

#     # HTML response for web
#     return send_file(output_filename, as_attachment=True, download_name=output_filename)

# if __name__ == '__main__':
#     app.run(debug=True)



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

import os
import math
import io
import requests
import gdown
from flask import Flask, request, jsonify, render_template, send_file
import speech_recognition as sr
from pydub import AudioSegment
import pyttsx3
import docx
import PyPDF2
import zipfile

# Function to check file existence and size
def is_file_up_to_date(destination, file_id):
    if os.path.exists(destination):
        # Get the size of the existing file
        existing_size = os.path.getsize(destination)
        print("existing_size  ",existing_size)
        # Get the size of the file on Google Drive
        drive_url = f'https://drive.google.com/uc?id={file_id}&export=download'
        response = requests.head(drive_url)
        drive_file_size = int(response.headers.get('Content-Length', 0))
        print("drive_file_size  ",drive_file_size)
        return existing_size == drive_file_size
    return False

def download_file_from_google_drive(file_id, destination):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, destination, quiet=False)

def download_ffmpeg():
    file_id = "1gKl_HiRnh8nKOrfm1FQyhHPoANA8GumK"  # Example file ID
    destination = "ffmpeg.zip"  # Desired destination filename
    ffmpeg_binaries_dir = "ffmpeg_binaries"  # Directory to extract the binaries

    # Check if the file already exists
    if os.path.exists(destination):
        actual_size = os.path.getsize(destination)
        expected_size = 59923823  # Update with the correct size in bytes

        if actual_size == expected_size:
            print(f"{destination} exists and is the correct size. No download needed.")
        else:
            print(f"{destination} exists but size is incorrect. Downloading...")
            download_file_from_google_drive(file_id, destination)
    else:
        print(f"{destination} does not exist. Downloading...")
        download_file_from_google_drive(file_id, destination)

    # Check if the destination directory exists, create if not
    if not os.path.exists(ffmpeg_binaries_dir):
        os.makedirs(ffmpeg_binaries_dir)

    # Check if the ffmpeg_binaries directory already contains the extracted files
    if any(file.endswith(('.exe', '.dll', '.so')) for file in os.listdir(ffmpeg_binaries_dir)):
        print(f"FFmpeg binaries already extracted to {ffmpeg_binaries_dir}. No extraction needed.")
    else:
        # Extract the downloaded ZIP file
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_binaries_dir)
            print(f"Extracted FFmpeg binaries to: {ffmpeg_binaries_dir}")

    # Optionally, remove the ZIP file after extraction
    # os.remove(destination)  # Uncomment if you want to delete the ZIP file after extraction

if __name__ == "__main__":
    download_ffmpeg()


# Set the path to the ffmpeg binary
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg_binaries", "ffmpeg")
AudioSegment.converter = ffmpeg_path  # Tell pydub to use the local ffmpeg binary

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
                    transcriptions.append(f"Chunk {i + 1} could not be understood.")
                except sr.RequestError:
                    transcriptions.append(f"Chunk {i + 1} had an API error.")

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
    voices = engine.getProperty('voices')
    if voice_id < len(voices):
        engine.setProperty('voice', voices[voice_id].id)
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

    if file and file.filename.endswith('.mp3'):
        try:
            audio = AudioSegment.from_mp3(file)
            transcription = transcribe_large_audio(audio)
            formatted_transcription = format_transcription(transcription)
        except Exception as e:
            formatted_transcription = f"Error during transcription: {str(e)}"

        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"transcription": transcription})
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

    if file.filename.endswith('.txt'):
        text = file.read().decode('utf-8')
    elif file.filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    elif file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    else:
        return jsonify({"error": "Invalid file format. Only txt, docx, and pdf allowed."}), 400 if request.is_json else render_template('text_to_audio.html', error="Invalid file format. Only txt, docx, and pdf allowed.")

    voice_id = int(request.form.get('voice', 0))
    speed = int(request.form.get('speed', 150))

    output_filename = "output_audio.mp3"
    convert_text_to_audio(text, output_filename, voice_id, speed)

    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({"message": "Text converted to audio", "filename": output_filename})
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
# import requests
# import zipfile

# # Function to handle large file download from Google Drive
# # def download_large_file_from_google_drive(file_id, destination):
# #     URL = "https://docs.google.com/uc?export=download"
# #     session = requests.Session()

# #     # Initial request to get the file and handle virus scan warning
# #     response = session.get(URL, params={'id': file_id}, stream=True)

# #     # Check if the response indicates that a confirmation token is needed
# #     token = get_confirm_token(response)
# #     if token:
# #         # Second request with the confirmation token
# #         params = {'id': file_id, 'confirm': token}
# #         response = session.get(URL, params=params, stream=True)

# #     # Save the file content to the destination
# #     save_response_content(response, destination)

# #     # Check the content of the downloaded file
# #     with open(destination, 'rb') as f:
# #         content = f.read(100)  # Read the first 100 bytes
# #         print("Downloaded content snippet:", content)

# #     # Validate if the downloaded content starts with a valid ZIP signature
# #     if content.startswith(b'PK'):  # ZIP files start with the bytes 'PK'
# #         print("Valid ZIP archive downloaded.")
# #     else:
# #         print("Downloaded file is not a valid ZIP archive.")

# import gdown

# def download_file_from_google_drive(file_id, destination):
#     # Construct the URL for downloading the file
#     url = f'https://drive.google.com/uc?id={file_id}'
    
#     try:
#         # Download the file using gdown
#         gdown.download(url, destination, quiet=False)
#         print(f"File downloaded successfully: {destination}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def download_ffmpeg():
#     # Replace with your actual file ID from Google Drive
#     file_id = "1gKl_HiRnh8nKOrfm1FQyhHPoANA8GumK"  # Example file ID
#     destination = "ffmpeg.zip"  # Desired destination filename
    
#     # Call the download function
#     download_file_from_google_drive(file_id, destination)

# if __name__ == "__main__":
#     download_ffmpeg()

# # Function to extract the confirmation token from cookies
# def get_confirm_token(response):
#     for key, value in response.cookies.items():
#         print("key ==>",key)
#         print("value ==>",value)
#         if key.startswith('download_warning'):
#             return value
#     return None

# # Function to save the response content to the destination file
# def save_response_content(response, destination):
#     CHUNK_SIZE = 32768
#     with open(destination, "wb") as f:
#         for chunk in response.iter_content(CHUNK_SIZE):
#             if chunk:
#                 f.write(chunk)



# # Set the path to the ffmpeg binary
# ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg_binaries", "ffmpeg")
# AudioSegment.converter = ffmpeg_path  # Tell pydub to use the local ffmpeg binary

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
# def convert_text_to_audio(text, filename, voice_id, speed):
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     if voice_id < len(voices):
#         engine.setProperty('voice', voices[voice_id].id)
#     engine.setProperty('rate', speed)
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
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     return render_template('text_to_audio.html', voices=voices)

# # API route for file upload and transcription
# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded."}), 400 if request.is_json else render_template('index.html', transcription="No file uploaded.")

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file."}), 400 if request.is_json else render_template('index.html', transcription="No selected file.")

#     if file and file.filename.endswith('.mp3'):
#         try:
#             audio = AudioSegment.from_mp3(file)
#             transcription = transcribe_large_audio(audio)
#             formatted_transcription = format_transcription(transcription)
#         except Exception as e:
#             formatted_transcription = f"Error during transcription: {str(e)}"

#         if request.headers.get('Content-Type') == 'application/json':
#             return jsonify({"transcription": transcription})
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

#     if file.filename.endswith('.txt'):
#         text = file.read().decode('utf-8')
#     elif file.filename.endswith('.docx'):
#         text = extract_text_from_docx(file)
#     elif file.filename.endswith('.pdf'):
#         text = extract_text_from_pdf(file)
#     else:
#         return jsonify({"error": "Invalid file format. Only txt, docx, and pdf allowed."}), 400 if request.is_json else render_template('text_to_audio.html', error="Invalid file format. Only txt, docx, and pdf allowed.")

#     voice_id = int(request.form.get('voice', 0))
#     speed = int(request.form.get('speed', 150))

#     output_filename = "output_audio.mp3"
#     convert_text_to_audio(text, output_filename, voice_id, speed)

#     if request.headers.get('Content-Type') == 'application/json':
#         return jsonify({"message": "Text converted to audio", "filename": output_filename})
#     return send_file(output_filename, as_attachment=True, download_name=output_filename)

# if __name__ == '__main__':
#     app.run(debug=True)
