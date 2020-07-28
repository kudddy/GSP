import atexit
from GeoService.ext.Pickler import PclWorker


class Memoize:

    def __init__(self, fn):
        self.fn = fn
        self.memo = PclWorker.get_pickle_file('GeoService/Cache/cache.p')
        atexit.register(self.dump)

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

    def dump(self):
        PclWorker.dump_pickle_file(self.memo, 'GeoService/Cache/cache.p')
