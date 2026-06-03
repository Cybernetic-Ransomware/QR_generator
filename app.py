import io
import os
import secrets

from flask import Flask, abort, render_template, request, send_file, jsonify
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from utils.logger import AppLogger
from utils.qr_generator import QRCodeGenerator
from utils.result_store import ResultStore


AppLogger.configure_logger()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024  # 5 MB image + multipart headroom
csrf = CSRFProtect(app)
store = ResultStore()


@app.errorhandler(413)
def request_too_large(e):
    return jsonify({'success': False, 'errors': ['File is too large. Maximum request size is 6 MB.']}), 413


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({'success': False, 'errors': ['Security token missing or expired. Please reload the page.']}), 400


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    size = int(request.form['size'])
    raw_image = request.files.get('image')
    image = raw_image if (raw_image and raw_image.filename) else None
    color = request.form.get('color') or None

    generator = QRCodeGenerator()
    success, errors = generator.generate_qr(text, size, image, color)

    if not success:
        return jsonify({'success': False, 'errors': errors})

    token = store.put({
        'qr': generator.qr_png,
        'artistic': generator.artistic_png,
        'artistic_ext': generator.artistic_ext,
    })
    return jsonify({'success': True, 'id': token})


@app.route('/result')
def result():
    token = request.args.get('id', '')
    payload = store.get(token)
    if payload is None:
        abort(404)
    return render_template(
        'result.html',
        token=token,
        qr_with_image_exists=payload['artistic'] is not None,
    )


@app.route('/download')
def download():
    token = request.args.get('id', '')
    payload = store.get(token)
    if payload is None:
        abort(404)
    return send_file(
        io.BytesIO(payload['qr']),
        mimetype='image/png',
        as_attachment=True,
        download_name='qr.png',
    )


@app.route('/download_with_image')
def download_with_image():
    token = request.args.get('id', '')
    payload = store.get(token)
    if payload is None or payload['artistic'] is None:
        abort(404)
    ext = payload['artistic_ext']
    mimetype = 'image/gif' if ext == 'gif' else 'image/png'
    return send_file(
        io.BytesIO(payload['artistic']),
        mimetype=mimetype,
        as_attachment=True,
        download_name=f'qr_with_image.{ext}',
    )


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=5000)
