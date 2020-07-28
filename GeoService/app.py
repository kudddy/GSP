import os
from termcolor import colored
import pickle
from flask import Blueprint, request
from flask_json import as_json
from GeoService.Geo.Distance import GetDistance
from GeoService.ext.Gdriver import Gdrive
from GeoService.ext.creds import token_filename
from GeoService.ext.helper import set_logger



TOKEN = 'shdfksdhflkdsfh'
logger = set_logger(colored('Deployment', 'green'))

if os.path.exists(token_filename):
    with open(token_filename, 'rb') as token:
        creds = pickle.load(token)

    logger.info('credentials succes download')

    logger.info('activate drive')
    drive = Gdrive(creds)
    logger.info('drive activate')
else:
    logger.critical('problems with credentials')

GetDistance = GetDistance()

GeoService = Blueprint('GeoService', __name__)


@GeoService.route('/get_nearest_city', methods=['POST'])
@as_json
def get_nearest_city():
    data = request.form if request.form else request.json

    if data.get('token') == TOKEN:
        input_city = data.get('data')
        input_city = input_city if input_city else None

        vac_or_city = data.get('get_vac')

        if input_city is None:
            return {
                'message': 'unknown data structure',
                'status': False
            }
        try:
            n_near_city = data.get('num_near_city')

            n_near_city = data.get('num_near_city') if n_near_city else 15
            # должен быть город юзера
            result = GetDistance.nearby_cities(input_city, n_near_city, get_vac=vac_or_city)

            return {
                'status': True,
                'data': result
            }

        except Exception as e:
            return {
                'status': False,
                'message': e
            }
    else:
        return {
            'message': 'authorization error',
            'status': False
        }
