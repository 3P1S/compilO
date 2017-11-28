import os
import subprocess
import sqlite3
from flask import Flask, request, redirect, jsonify, make_response
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["cpp", "cc"])
COMPILER_PATH = "/usr/bin/g++"
DB_TABLE = "table1"

app = Flask("compilO")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#  Use this to limit the upload size


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# This is the post method to upload the file.
@app.route('/submit/<username>', methods=['POST'])
def submit_file(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print ("Filename is: {0}".format(filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            compilation_file = app.config["UPLOAD_FOLDER"]+"/"+filename
            compilation_output = compile_cpp(username, compilation_file)
            print (compilation_output)
            return make_response(jsonify(result=compilation_output))
        return make_response(jsonify(status="upload failed"))


#  get all the compilation output
@app.route('/compilations', methods=['GET'])
def get_compilation_results():
    results_db = get_all_results(DB_TABLE)
    print (results_db)
    response = {}
    if results_db:
        for i in results_db:
            for j in range(2, len(i)):
                if i[j] != None:
                    response[i[0]] = i[j]
        return make_response(jsonify(status=response))

#  get compilation output by name
@app.route('/compilations/<username>', methods=['GET'])
def get_compilation_results_by_user(username):
    results_db = get_results_by_users(DB_TABLE, username)
    print(results_db)
    if results_db:
        response = {}
        for j in range(2, len(results_db)):
            if results_db[j] is not None:
                response[results_db[0]] = results_db[j]
        return make_response(jsonify(status=response))

#  get all the name of the students
@app.route('/getStudents', methods=['GET'])
def get_all_students():
    db = init_db()
    db_cursor = db.cursor()
    row = db_cursor.execute('SELECT USER_ID FROM {0}'.format(DB_TABLE)).fetchall()
    db.close()
    row = list(set(row))
    response_list = []
    for each in row:
        for element in each:
            response_list.append(element)
    print (response_list)
    return make_response(jsonify(status=response_list))

def compile_cpp(userID, file_name):
    #  executable_name =
    process = subprocess.Popen([COMPILER_PATH, "-Wall", "-o",
                               "executable", file_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    compilation_output = process.communicate()
    if compilation_output[1]:
        print("failed to compile")
        write_file_result_to_db(userID, file_name, DB_TABLE,
                compile_err=compilation_output[1])
        return compilation_output[1]
    process = subprocess.Popen(["./executable"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return_value = process.communicate()
    if return_value[1]:
        print("There was a runtime error!")
        write_file_result_to_db(userID, file_name, DB_TABLE,
                run_time_err=return_value[1])
        return return_value[1]
    write_file_result_to_db(userID, file_name, DB_TABLE,
            result=return_value[0])
    return return_value[0]


def init_db():
    # Add timeOut to close the db in case of slow connection, default is 5s.
    db_connect = sqlite3.connect("database.db")
    return db_connect


def create_table(table, db_cursor):
    # I guess you can also do "?" for the tabel name, make sure you get rid of {0}.
    first_half = "CREATE TABLE {0} (USER_ID TEXT NOT NULL, ".format(table) 
    query = first_half + "file BLOB NOT NULL, compile_error text, run_time_error text, result text)"
    try:
        db_cursor.execute(query)
    except sqlite3.OperationalError as error:
        if error.message == "table {0} already exists".format(DB_TABLE):
            print("Table already exists.")
        else:
            raise error


#  make sure to delete the file after adding it to db
def write_file_result_to_db(user_id, file_name, table, compile_err=None,
                            run_time_err=None, result=None):
    db = init_db()
    db_cursor = db.cursor()
    create_table(table, db_cursor)
    with open(file_name, "rb") as f:
        ablob = f.read()
    if compile_err:
        data = (user_id, buffer(ablob), compile_err, None, None)
    elif run_time_err:
        data = (user_id, buffer(ablob), None, run_time_err, None)
    elif result:
        data = (user_id, buffer(ablob), None, None, result)
    else:
        return -1
    db_cursor.execute("INSERT INTO {0} VALUES(?, ?, ?, ?, ?)".format(table),
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
        row = db_cursor.execute(
                "SELECT * FROM {0} WHERE USER_ID=?".format(table),
                data).fetchone()
        db.close()
        return row
    db.close()
    return "No user_id"


def get_all_results(table):
    db = init_db()
    db_cursor = db.cursor()
    row = db_cursor.execute("SELECT * FROM {0}".format(table)).fetchall()
    db.close()
    return row
