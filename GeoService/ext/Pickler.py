import pickle

'''
Класс для работы с сериализованными файлами
'''


class PclWorker:

    @staticmethod
    def get_pickle_file(filename: str):
        """
        Получение пикл файла
        """
        with open(filename, 'rb') as f:
            d_ = pickle.load(f)
        return d_

    @staticmethod
    def dump_pickle_file(obj, filename):
        """
        Дамп объекта
        Вход: объект, имя файла
        """
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)
