from flask import Flask, request
from flask_json import FlaskJSON, as_json
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from FastTextAsService.ext.Tokenizer import Tokenizer


class FastTextVectorizer(Tokenizer):
    def __init__(self, filename):
        super().__init__()
        self.fasttext_model = KeyedVectors.load(filename)

        self.vocab = self.fasttext_model.wv.vocab
        self.wv = self.fasttext_model.wv
        self.vector_size = self.fasttext_model.vector_size

        self.Z = 0
        for k in self.vocab:
            self.Z += self.vocab[k].count

    def get_mean_fasttext_vector(self, tokenized_doc):
        # создаем маски для векторов
        lemmas_vectors = np.zeros((len(tokenized_doc), self.fasttext_model.vector_size))

        # если слово есть в модели, берем его вектор
        for idx, lemma in enumerate(tokenized_doc):
            if lemma in self.fasttext_model.vocab:
                lemmas_vectors[idx] = self.fasttext_model.wv[lemma]
        return np.mean(lemmas_vectors, axis=0)

    def fit_transform(self, data):
        array = self.get_sif_vectors(data)
        return array

    def transform(self, data):
        return self.fit_transform(data)

    def get_sif_vectors(self, sents, is_tokenize=True, alpha=1e-3):

        output = []

        for s in sents:
            v = self.get_sif_vector(s, is_tokenize, alpha)
            output.append(v)
        return np.vstack(output)

    def get_sif_vector(self, tokenize_doc, is_tokenize=True, alpha=1e-3):
        count = 0
        v = np.zeros(self.vector_size)
        if is_tokenize:
            tokenize_doc = self.tokenize_line(tokenize_doc)
        for w in tokenize_doc:
            if w in self.vocab:
                v += (alpha / (alpha + (self.vocab[w].count / self.Z))) * self.wv[w]
                count += 1

        if count > 0:
            for i in range(self.vector_size):
                v[i] *= 1 / count
        return v


class FastTextAsServer:
    def __init__(self, fast_text_model, token, topn=30):

        self.TOKEN = token
        self.TOPN = topn

        self.fast_text_model = fast_text_model

    def create_flask_app(self):
        app = Flask(__name__)
        app.config['JSON_AS_ASCII'] = False

        @app.route('/get_vector', methods=['POST'])
        @as_json
        def get_vector():
            data = request.form if request.form else request.json
            if data.get('token') == self.TOKEN:
                input_data = data.get('data')
                input_data = input_data if input_data else input_data
                is_tokenize = data.get('is_tokenize')
                is_tokenize = False if is_tokenize is False else True
                try:
                    if (isinstance(input_data, list) and len(input_data)) \
                            and ((isinstance(input_data[0], list) and not is_tokenize)
                                 or (isinstance(input_data[0], str) and is_tokenize)):
                        result = self.fast_text_model.get_sif_vectors(input_data, is_tokenize)
                        return {
                            'status': 'ok',
                            'result': result
                        }
                    elif (isinstance(input_data, str) and is_tokenize) or (
                            isinstance(input_data, list) and not is_tokenize):
                        result = self.fast_text_model.get_sif_vector(input_data, is_tokenize)
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

        @app.route('/get_most_similar', methods=['POST'])
        @as_json
        def get_most_similar():
            data = request.form if request.form else request.json
            if data.get('token') == self.TOKEN:
                input_data = data.get('data')
                topn = data.get('topn')
                topn = topn if isinstance(topn, int) and topn > 0 else self.TOPN
                topn = topn if topn < 100 else 100
                if isinstance(input_data, str):
                    result = self.fast_text_model.wv.most_similar([input_data], topn=topn)
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

        FlaskJSON(app)

        return app

    def run(self, host='127.0.0.1', port=5001):
        app = self.create_flask_app()
        app.run(host=host, port=port, debug=True)
