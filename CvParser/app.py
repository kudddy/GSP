import os
from flask import jsonify
from os.path import join, dirname, realpath
from CvParser.ext.Parser import HhProfileInfo
from flask import Blueprint, request

hh = HhProfileInfo()

CvParser = Blueprint('CvParser', __name__)
ALLOWED_EXTENSIONS = set(['pdf'])

UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/')


def allowed_file(filename):
    return 'pdf' in filename


@CvParser.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):

        filename = 'temp.pdf'
        path = os.path.join(UPLOADS_PATH, filename)
        file.save(path)
        try:
            res = hh.get_vacants_ru(hh.read_pdf(path))
        except Exception as e:
            resp = jsonify({'status': 'file not recognized. Support only hh resume'})
            resp.status_code = 400
            return resp

        if res is None:
            resp = jsonify({'status': 'file not recognized. Support only hh resume'})
            resp.status_code = 400
            return resp
        resp = jsonify(res)
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'status': 'file not recognized. Support only hh resume'})
        resp.status_code = 400
        return resp
