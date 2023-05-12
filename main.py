from flask import Flask, jsonify,  request
import os
from flask_cors import CORS
from speech_analysis import main, individual_analysis

app = Flask(__name__)
CORS(app)
global_speech_file = 'indii_audio.wav'


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/sendaudio', methods=['POST', 'GET'])
def run_speechpost():
    data = "fileuploaded"
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'POST':
        audio_file = request.files['audFile']
        audio_file.save(global_speech_file)
        return "File Upload"
    else:
        return "In get request of /sendaudio endpoint"


@app.route('/getscores', methods=['GET'])
def run_speechget():
    data = "Sent Scores"
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return individual_analysis(global_speech_file)


@app.route('/data', methods=['POST', 'GET'])
def run_files():
    # data = "hello"
    # response = jsonify(data)
    # response.headers.add('Access-Control-Allow-Origin', '*')

    print('request.json', request.json)
    if request.method == 'POST':
        print('First')
        value = request.json.get('sessID')
        # user = request.json.get('userID')
        print('sessID', value)
        main(value)
        return "Added"
    else:
        return "In get request"


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
