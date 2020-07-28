import requests
from geographiclib.geodesic import Geodesic
from GeoService.ext.Pickler import PclWorker as pcl
from typing import List
from GeoService.ext.MemoCache import Memoize

geod = Geodesic.WGS84  # define the WGS84 ellipsoid


class GetDistance:
    def __init__(self):
        self.count = 0
        self.__lru = pcl.get_pickle_file('GeoService/Cache/coords.pickle')
        self.citys = pcl.get_pickle_file('GeoService/Cache/citys.p')

    @staticmethod
    def calc_distance(coord1, coord2):
        try:
            g = geod.Inverse(*coord1, *coord2)
        except Exception as e:
            return 10000000000000000000

        return g['s12'] / 1000

    @staticmethod
    @Memoize
    def get_coord(location):
        location = 'Россия,' + ' ' + location.lower()
        api_key = '3XNMb9DRSZDSHDzGNsMlVZZChOsEAFn5QSFuc-xSPsw'
        url = f'https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey={api_key}&searchtext={location}'
        get = requests.get(url)
        if get.status_code == 200:
            get = get.json()['Response']['View']
            if not get:
                return None
            coord = tuple(get[0]['Result'][0]['Location']['DisplayPosition'].values())
            return coord

    def _num_connection(self):
        return self.count

    def get_distance(self, city_one, city_two):
        if None in (city_one, city_two):
            return None
        coord_city_one = self.get_coord(city_one)

        coord_city_two = self.get_coord(city_two)

        return self.calc_distance(coord_city_one, coord_city_two)

    def nearby_cities(self, employe_city: str, n=15, get_vac=True) -> List[str]:
        local_dict = {}
        for city in self.citys.keys():
            dist = self.get_distance(employe_city, city)
            local_dict.update({city: dist})
        sorting_city = [x for x, y in sorted(local_dict.items(), key=lambda item: item[1])][:n]
        if get_vac:
            actual_vac = []
            for x in sorting_city:
                actual_vac.extend(self.citys[x])
            return actual_vac
        else:
            return sorting_city
