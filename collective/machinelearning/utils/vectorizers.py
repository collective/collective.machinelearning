from sklearn.feature_extraction.text import HashingVectorizer
import nltk.stem
import numpy as np
import scipy.linalg

from sklearn.feature_extraction.hashing import FeatureHasher
from sklearn.feature_extraction.hashing import _iteritems
from sklearn.feature_extraction import _hashing
import scipy.sparse as sp


def new_hashing_vectorizer(stop_words=None,
                           ngram_range=(1, 1),
                           nltk=False,
                           remembering=False):
    vecttype = HashingVectorizer
    if remembering:
        vecttype = VectorizerRemembering
    if nltk:
        vecttype = nltk_stemming(vecttype)
    return vecttype(stop_words=stop_words,
                    ngram_range=ngram_range)


def nltk_stemming(vectorizer_type):
    english_stemmer = nltk.stem.SnowballStemmer('english')

    class StemmedVectorizer(vectorizer_type):

        def build_analyzer(self):
            analyser = super(StemmedVectorizer, self).build_analyzer()
            return lambda doc: (english_stemmer.stem(w) for w in analyser(doc))

    return StemmedVectorizer


def nearers(vector, corpus):
    """
    Return the distance for each of corpus to vector
    """
    dists = []
    for i in range(corpus.shape[0]):
        dist = scipy.linalg.norm((vector - corpus[i]).toarray())
        dists.append((dist, i))

    return dists


# Modifying scikit-learn

class HasherRemembering(FeatureHasher):

    def transform(self, raw_X, y=None):
        raw_X = iter(raw_X)
        if self.input_type == "dict":
            raw_X = (_iteritems(d) for d in raw_X)
        elif self.input_type == "string":
            raw_X = (((f, 1) for f in x) for x in raw_X)
        indices, indptr, values = \
            _hashing.transform(raw_X, self.n_features, self.dtype)
        n_samples = indptr.shape[0] - 1

        if n_samples == 0:
            raise ValueError("Cannot vectorize empty sequence.")

        X = sp.csr_matrix((values, indices, indptr), dtype=self.dtype,
                          shape=(n_samples, self.n_features))
        X.sum_duplicates()  # also sorts the indices
        if self.non_negative:
            np.abs(X.data, X.data)

        # ADDING: PERSIST VALUES!
        self._indicespersisted = indices

        return X


class VectorizerRemembering(HashingVectorizer):

    def _get_hasher(self):
        # ADDING: PERSIST HASHER!
        self._hasherpersisted = HasherRemembering(
            n_features=self.n_features,
            input_type='string',
            dtype=self.dtype,
            non_negative=self.non_negative)
        return self._hasherpersisted

    def build_analyzer(self):
        analyser = super(VectorizerRemembering, self).build_analyzer()

        # ADDING: PERSIST STRINGS!
        self._stringspersisted = []

        def analyserremembering(doc):
            analysed = analyser(doc)
            self._stringspersisted += analysed
            return analysed

        return analyserremembering

    def get_feature_name(self, hashedfeature):
        try:
            idx = self._hasherpersisted._indicespersisted.tolist().index(
                hashedfeature)
            return self._stringspersisted[idx]
        except ValueError:
            return u'unknown'

    def get_feature_names(self):
        return {hashing: string for hashing, string in zip(
            self._hasherpersisted._indicespersisted,
            self._stringspersisted)}
