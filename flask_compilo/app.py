import os
#  import tarfile
import sqlite3
from flask import Flask, request, redirect, jsonify, make_response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'tar', '.cpp', 'cc', '.h', '.hpp'])

app = Flask("compilO")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#  Use this to limit the upload size
#  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def main_page():
    return 'hello world'


@app.route("/assign", methods=["POST"])
def hello():
    if request.method == "POST":
        return request.form['name']


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# This is the post method to upload the file.
@app.route('/submit', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response(jsonify(status="uploaded"))

#  def unzip_tar_file(file_to_unzip):
    #  tar = tarfile.open(file_to_unzip)
    #  tar.extractall('./uploads/extracts')
    #  tar.close()


def init_db():
    # Add timeOut to close the db in case of slow connection, default is 5s.
    db_connect = sqlite3.connect("database.db")
    return db_connect


def create_table(table):
    db = init_db()
    db_cursor = db.cursor()
    # TODO: Fix this shit, it's too long.
    # I guess you can also do "?" for the tabel name, make sure you get rid of {0}.
    query = "CREATE TABLE {0} (USER_ID  TEXT NOT NULL, assignment TEXT NOT NULL,".format(table) +
            "file BLOB NOT NULL, compile_error text, run_time_error text, result text)"
    db_cursor.execute(query)
    db.commit()
    db.close()

def write_file_result_to_db(user_id, assignment, file, table, compile_err=None,
                            run_time_err=None, result=None):
    db = init_db()
    db_cursor = db.cursor()
    if compile_err:
        data = (user_id, assignment, file, compile_err)
    elif run_time_err:
        data = (user_id, assignment, file, run_time_err)
    elif result:
        data = (user_id, assignment, file, result)
    else:
        return -1
    db_cursor.execute("INSERT INTO {0} VALUES(?, ?, ?, ?, ?, ?)".format(table),
                      data)
    db.commit()
    db.close()

#  implement this method if you decide to continue working on it later.
#  def clear_table():

def get_results_by_users(table, user_id):
    db = init_db()
    db_cursor = db.cursor()
    if user_id:
        data = (user_id,)
        row = db_cursor.execute("SELECT * FROM {0} WHERE USER_ID=?".format(table), data).fetchone()
        db.close()
        return row
    db.close()
    return "No user_id"

def get_all_results(table):
    db = init_db()
    db_cursor = db.cursor()
    row = db_cursor.execute("SELECT * FROM {0}".format(table)).fetchone()
    db.close()
    return row





