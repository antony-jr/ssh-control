import tempfile
import os
import uuid
from flask import Flask,jsonify,render_template,send_file,redirect,request
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg'}
storedir = '{}/Uploaded/'.format(os.path.expanduser('~'))

app = Flask("Optical Braille Recognition Demo")
app.config['UPLOAD_FOLDER'] = storedir

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def fav():
    return send_file('favicon.ico', mimetype='image/ico')

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error" : True, "message" : "file not in request"})
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": True, "message" : "empty filename"})
    if file and allowed_file(file.filename):
        filename = '{}'.format(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        r = {
                "error": False,
                "message": "File Uploaded Successfully"
        }
        return jsonify(r)

if __name__ == "__main__":
    app.run()
