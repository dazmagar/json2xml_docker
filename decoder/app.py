from flask import Flask, request, render_template, url_for
from helpers.common import random_string
from glob import glob

import base64
import os

app=Flask(__name__, static_folder='static', template_folder='template')

app.secret_key = random_string(16)
app.config['ENCODED_FOLDER'] = "./encoded"
app.config['RESULT_FOLDER'] = "./static"

@app.route('/')
def upload_form():
    return render_template('getxml.html')

@app.route('/', methods=['POST'])
def decode_files():
    if request.method == 'POST':

        if os.path.exists(app.config['RESULT_FOLDER']):
            for f in os.listdir(app.config['RESULT_FOLDER']):
                os.remove(os.path.join(app.config['RESULT_FOLDER'], f))
        else:
            os.makedirs(app.config['RESULT_FOLDER'])

        encoded_files = [os.path.normpath(file) for file in glob(app.config['ENCODED_FOLDER'] + '/*data')]

        for file in encoded_files:
            with open(file, 'r') as f:
                encoded_content = f.read()
            
            result_file = os.path.join(app.config['RESULT_FOLDER'], f"{random_string(8)}_data.xml")
            with open(result_file, 'w') as f:
                f.write(base64.b64decode(encoded_content).decode('utf-8'))
                f.close()

        decoded_files = [os.path.basename(file_path) for file_path in glob(app.config['RESULT_FOLDER'] + '/*.xml')]
        return render_template('file_structure.html', links=decoded_files)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
