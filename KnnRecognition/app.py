from flask import Blueprint, request
from flask_json import as_json
from FastTextAsService.constant.secrets import TOKEN, path_model_knn
from GeoService.ext.Pickler import PclWorker as pcl
from FastTextAsService.app import fast_text_model

KnnRecognition = Blueprint('KnnRecognition', __name__)
knn_clf = pcl.get_pickle_file(path_model_knn)
mapping = {0: 'да', 1: 'нет'}


@KnnRecognition.route('/get_answer', methods=['POST'])
@as_json
def get_answer():
    data = request.form if request.form else request.json
    if data.get('token') == TOKEN:
        print('мы тут')
        try:
            input_data = data.get('data')
            vector = fast_text_model.wv.get_vector(input_data)
            response = mapping[knn_clf.predict([vector])[0]]
            return {
                'status': True,
                'result': response
            }
        except Exception as e:
            return {
                'status': False,
                'error': str(e)
            }
    else:
        return {'status': 403}
