from flask import Flask, jsonify, request
from file_service import audio_file_details, upload_to_gcs
import file_service as fs

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload():
    f = request.files['file']
    file_uri = upload_to_gcs(f)

    # Construct audio file meta data
    meta_data = audio_file_details(f)
    meta_data['uri'] = file_uri

    return jsonify(meta_data)

if __name__ == "__main__":
    app.run(port=8000)