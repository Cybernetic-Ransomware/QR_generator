import os

from flask import Flask, render_template, request, send_file, jsonify
from utils.logger import AppLogger
from utils.qr_generator import QRCodeGenerator


AppLogger.configure_logger()

app = Flask(__name__)


def before_request_index():
    file_names = ('qr', 'qr_with_image')
    current_dir = os.listdir()

    for filename in current_dir:
        for name in file_names:
            if filename.startswith(name):
                try:
                    os.remove(filename)
                except Exception as e:
                    AppLogger.logger.error(f"Error removing file {filename}: {e}")


@app.route('/')
def index():
    before_request_index()
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    size = int(request.form['size'])
    image = request.files['image'] if 'image' in request.files else None
    color = request.form['color'] if 'color' in request.form else None

    generator = QRCodeGenerator()
    success, errors = generator.generate_qr(text, size, image, color)

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'errors': errors})


@app.route('/result')
def result():
    qr_with_image_exists = any(filename.startswith('qr_with_image') for filename in os.listdir('.'))
    return render_template('result.html', qr_with_image_exists=qr_with_image_exists)


@app.route('/download')
def download():
    return send_file('qr.png', as_attachment=True)


@app.route('/download_with_image')
def download_with_image():
    for filename in os.listdir('.'):
        if filename.startswith('qr_with_image'):
            return send_file(filename, as_attachment=True)

    return "File not found", 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
