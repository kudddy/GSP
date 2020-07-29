from flask import Flask
from flask_json import FlaskJSON
from FastTextAsService.app import FastTextAsServer
from GeoService.app import GeoService
from CvParser.app import CvParser
from KnnRecognition.app import KnnRecognition
UPLOAD_FOLDER = 'CvParser/uploads'
app = Flask(__name__)

app.register_blueprint(FastTextAsServer, url_prefix='/FastTextAsServer')
app.register_blueprint(GeoService, url_prefix='/GeoService')
app.register_blueprint(CvParser, url_prefix='/CvParser')
app.register_blueprint(KnnRecognition, url_prefix='/KnnRecognition')
app.config['JSON_AS_ASCII'] = False
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def hello():
    return 'status ok'


app = FlaskJSON(app)

# app.run(host='0.0.0.0', port=5000, debug=False)
