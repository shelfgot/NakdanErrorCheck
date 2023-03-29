import os, glob
from processtext import *
from flask import Flask, flash, request, redirect, url_for, g, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def serve_process_page():
    f_path = ""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(f_path)
            return render_template('main.html', get_suggestions=compile_suggestions, f=f_path)
    return '''
    <!doctype html>
    <h1>Upload file for analysis</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/stop')
def clear_upload_folder():
    files = glob.glob('./temp/*')
    for f in files:
        os.remove(f)