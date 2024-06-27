import os
from os import path
from os.path import realpath
import logging
import sys

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

import audio_id_code

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


app = Flask(__name__)

# Set up directories relative to the current working directory
BASE_DIR = realpath(path.dirname(path.abspath(__file__)))
INDEX_UPLOAD_FOLDER = realpath(path.join(
    BASE_DIR, '..', 'uploads', 'index'))
QUERY_UPLOAD_FOLDER = realpath(path.join(
    BASE_DIR, '..', 'uploads', 'query'))
os.makedirs(INDEX_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QUERY_UPLOAD_FOLDER, exist_ok=True)
app.config['INDEX_UPLOAD_FOLDER'] = INDEX_UPLOAD_FOLDER
app.config['QUERY_UPLOAD_FOLDER'] = QUERY_UPLOAD_FOLDER


logger.info(f'{__name__} Loaded, python-version: {sys.version} {app.config=}')


def get_filename(request):
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    return secure_filename(file.filename), 200


# Testing hack
do_query = None


@app.route('/api/index', methods=['POST'])
@app.route('/index', methods=['POST'])
def index():
    s, ret_code = get_filename(request)
    if ret_code != 200:
        return s, ret_code

    filename = s
    path_str = realpath(path.join(app.config['INDEX_UPLOAD_FOLDER'], filename))

    file = request.files['file']

    file.save(path_str)

    logger.info(f'index saved: {path_str}')

    info = audio_id_code.index_file(path_str)

    return (
        jsonify({
            "message": f"File successfully uploaded to {filename}",
            "info": info},
            ),
        200)


@app.route('/api/query', methods=['POST'])
@app.route('/query', methods=['POST'])
def query():
    s, ret_code = get_filename(request)
    if ret_code != 200:
        return s, ret_code

    filename = s
    path_str = realpath(path.join(app.config['QUERY_UPLOAD_FOLDER'], filename))

    file = request.files['file']

    logger.info(f'query saved: {path_str}')

    file.save(path_str)
    logger.info(f'upload completed: saved as {path_str}')
    choice_info, stats = audio_id_code.query_all(path_str)

    num_matches, offset_sec = do_query(path_str)
    return (
        jsonify({
            "message": f"File successfully uploaded to {filename}",
            "stats": stats,
            "choice": choice_info,}),
        200)



@app.route('/api/index_1', methods=['POST'])
def index_1():
    s, ret_code = get_filename(request)
    if ret_code != 200:
        return s, ret_code

    filename = s
    path_str = realpath(path.join(app.config['INDEX_UPLOAD_FOLDER'], filename))

    file = request.files['file']

    file.save(path_str)

    logger.info(f'index saved: {path_str}')
    global do_query
    do_query = audio_id_code.tst(path_str)

    return (
        jsonify({"message": f"File successfully uploaded to {filename}"}),
        200)


@app.route('/api/query_1', methods=['POST'])
def query_1():
    s, ret_code = get_filename(request)
    if ret_code != 200:
        return s, ret_code

    filename = s
    path_str = realpath(path.join(app.config['QUERY_UPLOAD_FOLDER'], filename))

    file = request.files['file']

    logger.info(f'query saved: {path_str}')

    file.save(path_str)
    logger.info('upload completed')

    num_matches, offset_sec = do_query(path_str)
    return (
        jsonify({
            "message": f"File successfully uploaded to {filename}",
            "num_matches": num_matches,
            "offset_sec": offset_sec}),
        200)



@app.route('/audio_db')
def audio_db():
    files = os.listdir(app.config['INDEX_UPLOAD_FOLDER'])
    return render_template('audio_db.html', files=files)


@app.route('/api/audio_db')
def api_audio_db():
    files = os.listdir(app.config['INDEX_UPLOAD_FOLDER'])
    return jsonify({"files": files})


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
