from flask import Flask, jsonify, request
from file_service import audio_file_details, upload_to_gcs, async_transcribe, poll_operation
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

@app.route('/api/transcribe', methods=['GET'])
def transcribe():
    params = request.get_json()
    operation = async_transcribe(params['uri'], params['sampling_rate'], params['channels'])
    return operation

@app.route('/api/operation/<name>', methods=['GET'])
def operation_status(name):
    response = poll_operation(name)
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=8000)