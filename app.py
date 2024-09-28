import os
import math
import io
from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which

# Set up ffmpeg path for pydub
AudioSegment.converter = which("ffmpeg")

app = Flask(__name__)

# Function to handle large audio files and transcription
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

# # Format the transcription result into readable paragraphs
# def format_transcription(transcription):
#     sentences = transcription.split(". ")
#     formatted_transcription = "<br><br>".join(sentences) + "."  # Add double line break between sentences
#     return formatted_transcription

def format_transcription(transcription):
    # Split the transcription into sentences based on full stops and line breaks
    sentences = transcription.split('. ')
    
    # Group sentences into paragraphs (e.g., 3 sentences per paragraph)
    paragraph_length = 3
    paragraphs = [" ".join(sentences[i:i + paragraph_length]) for i in range(0, len(sentences), paragraph_length)]
    
    # Join paragraphs with double line breaks to create readable spacing
    formatted_transcription = "<br><br>".join(paragraphs) + "."
    return formatted_transcription



# Frontend route for file upload page
@app.route('/')
def index():
    return render_template('index.html')

# API route for file upload and transcription
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return render_template('index.html', transcription="No file uploaded."), 400

    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', transcription="No selected file."), 400

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

        # If the request comes from an API client, return JSON response
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"transcription": transcription})

        # Default response to render HTML page with transcription
        return render_template('index.html', transcription=formatted_transcription)
    else:
        return render_template('index.html', transcription="Invalid file format. Only MP3 allowed."), 400

if __name__ == '__main__':
    app.run(debug=True)
