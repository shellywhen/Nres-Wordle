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
    print(request.files)
    file = request.files['file']
    form = request.get_json()
    print(form, file)
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
