from flask import Flask, render_template, request, send_file
import os
from PIL import Image
import pytesseract
import pyttsx3
import PyPDF2

def select(gender, speed_option, text, output_file):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if gender.lower() == 'male':
        engine.setProperty('voice', voices[0].id)
    elif gender.lower() == 'female':
        engine.setProperty('voice', voices[1].id)
    if speed_option.lower() == 'slow':
        engine.setProperty('rate', 100)
    elif speed_option.lower() == 'normal':
        engine.setProperty('rate', 150)
    elif speed_option.lower() == 'medium':
        engine.setProperty('rate', 175)
    elif speed_option.lower() == 'fast':
        engine.setProperty('rate', 200)
    engine.save_to_file(text, output_file + '.mp3')
    engine.runAndWait()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/imgtoaudio')
def imgtoaudio():
    return render_template('imgtotext.html')
@app.route('/pdftoaudio')
def pdftoaudio():
    return render_template('pdftotext.html')
@app.route('/texttoaudio')
def texttoaudio():
    return render_template('texttoaudio.html')

@app.route('/imgtoaudio', methods=['POST'])
def upload():
    image_file = request.files['file']
    speed_option = request.form['speeds']
    gender = request.form['tones']
    output_file = request.form['output_file']
    image_path = 'static/images/uploaded_image.png'
    image_file.save(image_path)
    text = pytesseract.image_to_string(Image.open(image_path))

    
    select(gender, speed_option, text, output_file )
    
    audio_path = output_file + '.mp3'
    return send_file(audio_path, as_attachment=True, mimetype='audio/mpeg', download_name=output_file + '.mp3')


@app.route("/ptoa", methods = ['POST'])
def ptoa():
    file = request.files['file']
    start = request.form['start']
    end = request.form['end']
    def extract_text_from_pdf(pdf_path, start, end):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            if end > num_pages:
                end = num_pages
            text = ''
            for page_number in range(start, end):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()

        return text
    pdf_path = 'static/images/uploaded_pdf.pdf'
    file.save(pdf_path)
    
    extracted_text = extract_text_from_pdf(pdf_path, int(start), int(end))
    speed_option = request.form['speeds']
    gender = request.form['tones']
    output_file = request.form['output_file']
    select(gender, speed_option, extracted_text, output_file)
    audio_path = output_file + '.mp3'
    return send_file(audio_path, as_attachment=True, mimetype='audio/mpeg', download_name=output_file + '.mp3')
@app.route("/ttoa", methods = ['POST'])
def ttoa():
    text = request.form['text']
    speed_option = request.form['speeds']
    gender = request.form['tones']
    output_file = request.form['output_file']
    select(gender, speed_option, text, output_file)
    audio_path = output_file + '.mp3'
    return send_file(audio_path, as_attachment=True, mimetype='audio/mpeg', download_name=output_file + '.mp3')
if __name__ == '__main__':
    app.run(debug=True)
