from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Set up directories relative to the current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads', 'index')
QUERY_UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads', 'query')
os.makedirs(INDEX_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QUERY_UPLOAD_FOLDER, exist_ok=True)
app.config['INDEX_UPLOAD_FOLDER'] = INDEX_UPLOAD_FOLDER
app.config['QUERY_UPLOAD_FOLDER'] = QUERY_UPLOAD_FOLDER


@app.route('/api/index', methods=['POST'])
@app.route('/index', methods=['POST'])
def index():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        filename = os.path.join(
            app.config['INDEX_UPLOAD_FOLDER'],
            file.filename)
        file.save(filename)
        return (
            jsonify({"message": f"File successfully uploaded to {filename}"}),
            200)


@app.route('/api/query', methods=['POST'])
@app.route('/query', methods=['POST'])
def query():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        filename = os.path.join(
            app.config['QUERY_UPLOAD_FOLDER'],
            file.filename)
        file.save(filename)
        return (
            jsonify({"message": f"File successfully uploaded to {filename}"}),
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
