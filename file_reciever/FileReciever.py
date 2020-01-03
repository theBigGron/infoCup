from flask import Flask, request, redirect, Response
from werkzeug.datastructures import FileStorage
import uuid
import tarfile

import sqlite3

"""
    From
    https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
"""
DATABASE = "../models.db"


UPLOAD_FOLDER = '/home/pag/Development/infcmodelmerger/pytorch_models/model_staging/'
ALLOWED_EXTENSIONS = {'pth', 'tar'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MODEL_TYPES = ["actor_target", "actor", "critic_target", "critic"]
MODEL_CLASSES = ["city", "disease"]

sql_create_table = """ CREATE TABLE IF NOT EXISTS models (
                            model_class text,
                            model_type text,
                            id text,
                            model blob,
                            PRIMARY KEY(id, model_class, model_type)
                            );
                    """

sql_create_ref_table = """ CREATE TABLE IF NOT EXISTS max_model (
                            model_class text,
                            model_type text,
                            model blob,
                            PRIMARY KEY(model_class, model_type)
                            );
                    """

sql_replace_model = """ REPLACE INTO models VALUES (?,?,?,?); """


def setup():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(sql_create_table)
    c.execute(sql_create_ref_table)
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_model(model: tarfile, model_info, client_id):
    for type in MODEL_TYPES:
        if type in model_info:
            model_type = type
            break

    for class_ in MODEL_CLASSES:
        if class_ in model_info:
            model_class = class_
            break

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    bin_mod = model.read()
    c.execute(sql_replace_model, (str(model_class), str(model_type), str(client_id), bin_mod))
    conn.commit()
    conn.close()


def save_file(file: FileStorage, client_id):
    models = tarfile.open(fileobj=file.stream, mode="r")

    for model_info in models:
        print(model_info.name)

        save_model(models.extractfile(model_info), model_info.name, client_id)
    return


@app.route('/models', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        try:
            client_id = request.headers.environ["HTTP_AUTHORIZATION"].replace("Basic", "").strip()
        except KeyError:
            print("No authorization")
            return "Set Authorization Header"

        if file and allowed_file(file.filename):
            save_file(file, client_id)
            return 'File Recieved'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/get-id', methods=['GET'])
def return_id():
    if request.method == 'GET':
        return Response(str(uuid.uuid4()), mimetype="text/plain")


@app.route('/get-model', methods=['GET'])
def return_model():
    if request.method == 'GET':
        return "Not implemented"


if __name__ == '__main__':
    setup()
    app.run(debug=True, host='0.0.0.0', port=8087, threaded=True)
