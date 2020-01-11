import sqlite3
import tarfile
import uuid

from flask import Flask, request, redirect, Response, send_file, abort
from werkzeug.datastructures import FileStorage

from common.data_processing.tar_buffer import merge_models_tar_to_buffered_tar
from master.src.ModelMerger import ModelMerger

"""
    From
    https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
"""

DATABASE = "./models.db"
ALLOWED_EXTENSIONS = {'pth', 'tar'}
MODEL_TYPES = ["actor_target", "actor", "critic_target", "critic"]
MODEL_CLASSES = ["city", "disease"]

sql_create_models_table = """ CREATE TABLE IF NOT EXISTS models (
                            model_type text,
                            id text,
                            model blob,
                            PRIMARY KEY(id, model_type)
                            );
                          """

sql_create_ref_table = """ CREATE TABLE IF NOT EXISTS max_model (
                            model_type text,
                            model blob,
                            PRIMARY KEY(model_type)
                            );
                       """

sql_create_settings_table = """ CREATE TABLE IF NOT EXISTS settings (
                                 id INTEGER PRIMARY KEY CHECK (id = 0),
                                 exploration float
                                 );
                            """

sql_set_exploration = """ REPLACE INTO settings VALUES ("id"=0,?);"""
sql_get_exploration = """ SELECT exploration FROM settings WHERE "id"=0; """
sql_get_ref_models = """ SELECT * FROM max_model; """
sql_replace_model = """ REPLACE INTO models VALUES (?,?,?); """

app = Flask(__name__)


def setup_db() -> None:
    """
    Creates sqliteDB and base models.

    :return: None
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(sql_create_models_table)
    c.execute(sql_create_ref_table)
    c.execute(sql_create_settings_table)
    c.execute(sql_set_exploration, [1])
    conn.commit()
    conn.close()


def allowed_file(filename: str) -> bool:
    """
    Checks if the file type is an acceptable filetype.

    :param filename: Name of file.
    :return: Weather or not we allow acceptance of that file.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_model(model: tarfile, model_info: tarfile.TarInfo, client_id: uuid.UUID) -> None:
    """
    Saves file in database.

    :param model: Tarfile containing a model.
    :param model_info: TarInfo regarding the model.
    :param client_id: Id from where the model came. Overwrites model in database.
    :return: None
    """
    for type_ in MODEL_TYPES:
        if type_ in model_info:
            model_type = type_
            break

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    bin_mod = model.read()
    c.execute(sql_replace_model, (str(model_type), str(client_id), bin_mod))
    conn.commit()
    conn.close()


def save_file(file: FileStorage, client_id: uuid.UUID) -> None:
    """
    Saves the data from buffer.

    :param file: Buffer saving data recieved.
    :param client_id: Unique ID to indentify source.
    :return: None
    """
    models = tarfile.open(fileobj=file.stream, mode="r")

    for model_info in models:
        save_model(models.extractfile(model_info), model_info.name, client_id)
    return


@app.route('/models', methods=['GET', 'POST'])
def upload_file() -> str:
    """
    Used to recieve newly trained models.
    :return: Response message to be send to client by flask.
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'models' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['models']
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
    return '''No File recieved or wrong method.'''


@app.route('/get-id', methods=['GET'])
def return_id():
    """
    Generates a random id.

    Is used later to overwrite models recieved from the same client.

    :return: UNIQUE id as string.
    """
    if request.method == 'GET':
        return Response(str(uuid.uuid4()), mimetype="text/plain")


@app.route('/get-exploration', methods=['GET'])
def return_explo():
    """
    Returns an exploration rate between 0 and 1.

    Used by slave to update their exploration rate.
    :return: Exploration rate between 0 and 1
    """
    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        explo = c.execute(sql_get_exploration).fetchone()[0]
        conn.close()
        return str(explo)


@app.route('/set-exploration', methods=['GET', 'POST'])
def set_explo():
    """
    Used to update the exploration rate. Used by scientists.
    :return: Success message if successful.
    """
    if request.method == 'POST':
        try:
            req = request
            rate_str = req.form["exploration_rate"]
            new_explo_rate = float(rate_str)
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute(sql_set_exploration, [new_explo_rate])
            conn.commit()
            conn.close()
        except Exception:
            # return internal server error
            return abort(500)
        return "Updated exploration rate successful."


@app.route('/get-model', methods=['GET'])
def return_model():
    """
    Returns current reference model for the slaves to improve.

    :return: TarFile Containing multiple models.
    """
    if request.method == 'GET':
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute(sql_get_ref_models)
            models = c.fetchall()
            conn.commit()
            conn.close()
            outer_tar_buffer = merge_models_tar_to_buffered_tar(models)
            return send_file(outer_tar_buffer,
                             mimetype="application/tar",
                             as_attachment=True,
                             attachment_filename="models.tar")
        except Exception:
            abort(500)


if __name__ == '__main__':
    setup_db()
    model_merger = ModelMerger(DATABASE, MODEL_CLASSES, MODEL_TYPES)
    model_merger.start()
    app.run(debug=True, host='0.0.0.0', port=8087, threaded=True)
