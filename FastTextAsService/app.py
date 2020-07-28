from FastTextAsService.ext.FastTextAsService import FastTextVectorizer
import os
import pickle
from FastTextAsService.constant.secrets import file_one, file_there, file_two, path_model, TOKEN, TOPN
from FastTextAsService.ext.helper import set_logger
from termcolor import colored
from FastTextAsService.ext.Gdriver import Gdrive

from flask import Blueprint, request
from flask_json import as_json

logger = set_logger(colored('Deployment', 'green'))

if os.path.exists('FastTextAsService/cache/token.pickle'):
    with open('FastTextAsService/cache/token.pickle', 'rb') as token:
        creds = pickle.load(token)

    logger.info('credentials succes download')

    logger.info('activate drive')
    drive = Gdrive(creds)
    logger.info('drive activate')
else:
    logger.critical('problems with credentials')

if os.path.exists(path_model):
    fast_text_model = FastTextVectorizer(path_model + file_one[1])
    logger.info('model work fine')
else:
    logger.info('model not found')
    logger.info('make dir')
    os.makedirs(path_model, mode=0o777, exist_ok=False)

    logger.info('upload files')
    drive.DwnldFileById(file_one[0], path_model + file_one[1])

    drive.DwnldFileById(file_two[0], path_model + file_two[1])

    drive.DwnldFileById(file_there[0], path_model + file_there[1])

    logger.info('upload success')

    fast_text_model = FastTextVectorizer(path_model + file_one[1])

    logger.info('model work fine')

logger.info('start FastTextAsServer')


FastTextAsServer = Blueprint('FastTextAsServer', __name__)


@FastTextAsServer.route('/get_vector', methods=['POST'])
@as_json
def get_vector():
    data = request.form if request.form else request.json
    if data.get('token') == TOKEN:
        input_data = data.get('data')
        input_data = input_data if input_data else input_data
        is_tokenize = data.get('is_tokenize')
        is_tokenize = False if is_tokenize is False else True
        try:
            if (isinstance(input_data, list) and len(input_data)) \
                    and ((isinstance(input_data[0], list) and not is_tokenize)
                         or (isinstance(input_data[0], str) and is_tokenize)):
                result = fast_text_model.get_sif_vectors(input_data, is_tokenize)
                return {
                    'status': 'ok',
                    'result': result
                }
            elif (isinstance(input_data, str) and is_tokenize) or (
                    isinstance(input_data, list) and not is_tokenize):
                result = fast_text_model.get_sif_vector(input_data, is_tokenize)
                return {
                    'status': 'ok',
                    'result': [result]
                }
        except:
            return {
                'status': 'unknown error'
            }
        return {
            'status': 'unknown data structure'
        }
    else:
        return {
            'status': 'authorization error'
        }


@FastTextAsServer.route('/get_most_similar', methods=['POST'])
@as_json
def get_most_similar():
    data = request.form if request.form else request.json
    if data.get('token') == TOKEN:
        input_data = data.get('data')
        topn = data.get('topn')
        topn = topn if isinstance(topn, int) and topn > 0 else TOPN
        topn = topn if topn < 100 else 100
        if isinstance(input_data, str):
            result = fast_text_model.wv.most_similar([input_data], topn=topn)
            return {
                'status': 'ok',
                'result': result
            }
        else:
            return {
                'status': 'unknown data structure'
            }
    else:
        return {
            'status': 'authorization error'
        }

