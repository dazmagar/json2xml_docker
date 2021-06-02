from flask import Flask, flash, request, redirect, render_template
from helpers.common import random_string

import dicttoxml
import base64
import json
import os

app=Flask(__name__, template_folder='template')

app.secret_key = random_string(16)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ENCODED_FOLDER'] = "./encoded"

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if os.path.exists(app.config['ENCODED_FOLDER']):
            for f in os.listdir(app.config['ENCODED_FOLDER']):
                os.remove(os.path.join(app.config['ENCODED_FOLDER'], f))
        else:
            os.makedirs(app.config['ENCODED_FOLDER'])

        if 'files[]' not in request.files:
            flash('No files')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            data_dict = json.loads(file.read().decode('utf-8'))
            data_xml = dicttoxml.dicttoxml(data_dict)
            result_file = os.path.join(app.config['ENCODED_FOLDER'], f"{random_string(8)}_data")
            with open(result_file, 'wb') as f:
                f.write(base64.b64encode(data_xml))
                f.close()

        flash('File(s) uploaded')
        return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
