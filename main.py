from flask import Flask, jsonify,  request
import os
from flask_cors import CORS
from speech_analysis import main

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/data',  methods=['POST', 'GET'])
def run_files():

    print('request.json', request.json)
    if request.method == 'POST':
        print('First')
        value = request.json.get('sessID')
        user = request.json.get('userID')
        print('sessID', value)
        print('userID', user)

        main(value, user)
        return "Added"
    else:
        return "In get request"


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
