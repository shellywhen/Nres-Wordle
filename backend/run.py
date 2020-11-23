from flask import Flask, send_file, request, jsonify, send_from_directory
from dataHandler import dataService
from flask_cors import CORS, cross_origin
import simplejson
import os

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
ds = dataService.dataHandler
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")

@app.route('/data')
@cross_origin()
def data():
    data = ds.getAll()
    return simplejson.dumps(data, ignore_nan=False)

@app.route('/dataHandler', methods=['POST'])
@cross_origin()
def dataHandler():
    form = request.get_json()
    print(form)
    data = ds.handleForm(form)
    return simplejson.dumps(data, ignore_nan=False)

@app.route('/generated/<key>')
@cross_origin()
def generated(key):
    try:
        return send_file('data/'+key, as_attachment=True)
    except:
        return('')
    return send_file()

@app.route('/file_upload/<type>', methods=['GET', 'POST'])
@cross_origin()
def file_upload(t):
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            print(t, filename)
            file.save(f'file/{file.filename}')
            return 'ok'

@app.route('/data_request',  methods=['POST'])
@cross_origin()
def data_request():
    form = request.get_json()['configure']
    print(form)
    data = ds.getData(form)
    return simplejson.dumps(data, ignore_nan=False)

@app.route('/word_request', methods=['POST'])
def word_request():
    form = request.get_json()['configure']
    period = request.get_json()['period']
    data = ds.getCount(period)
    return simplejson.dumps(data, ignore_nan=False)

app.run(host='0.0.0.0', port=1111, use_reloader=False, debug=True)
