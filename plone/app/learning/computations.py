import os.path

from plone.app.learning.vectorizer import Vectorizer
from plone.app.learning.clustering import Clustering
from plone.app.learning.utils.base import CatalogEmpty
from plone.app.learning.interfaces import ILearningString


MODELS = [Clustering, ]


class Learning(object):

    """
    Compute the Machine Learning model
    """

    def __init__(self, context, schema, vectorizer=Vectorizer, models=MODELS):
        """
        :param context: A Machine learning model
        :param schema: The schema of the model
        :param vectorizer: The model for the Vectorizer
        :param models: A list of machine learning models
        """
        self.context = context
        self.schema = schema
        self.vectmodel = vectorizer
        self.models = MODELS
        self._computed_results = []

    def _validate_schema(self):
        """
        Check the parametres of the schema.
        Returns None when parametres are correct.
        Returns an error string otherwise.
        """
        if not os.path.exists(self.schema.modelsDir):
            return 'Directory path does not exist {}'.format(
                self.schema.modelsDir)
        return

    def _compute_action(self, persist=False):
        errors = self._validate_schema()
        if errors:
            return errors
        status = ''
        errors = self._validate_schema()
        if errors:
            return errors

        # 1. Compute the vectorizer
        obj_vector = self.vectmodel(self.context, self.schema)
        try:
            vectorizer, corpus = obj_vector.iterator_learning_attributes()
        except CatalogEmpty as m:
            return m
        contents = obj_vector.learned_objs
        nsamples, nfeatures = corpus.shape
        nfeatures = corpus.nnz  # Real features in case of HashingVectorizer
        r = 'Recomputed vectorizer. Samples: {0}. Features: {1}.\n'.format(
            nsamples, nfeatures)
        status += r

        # 2. Compute the models
        for model in self.models:
            obj_model = model(self.context, self.schema)
            status += obj_model.compute(vectorizer, corpus, persist)
            results = obj_model.get_results()
            if persist and results is not None:
                # persist results for the models that have results
                for ob, label in zip(contents, results):
                    obj_model.persist_result(ob, label)
            else:
                self._computed_results.append({
                    'model': obj_model.__class__,
                    'results': [
                        (ob.UID(), label)
                        for ob, label in zip(contents, results)
                    ]
                })

        # 3. Information
        return status

    def compute(self):
        """
        Compute the Machine Learning model and persist
        """
        status = self._compute_action(persist=True)
        return status

    def get_results(self):
        """
        Get the results without persisting the Machine Learning model
        """
        self._compute_action(persist=False)
        return self._computed_results


# Predict with the model
class Predict(object):

    def __init__(self, context, schema, vectorizer=Vectorizer, models=MODELS):
        """
        :param context: A Machine learning model
        :param schema: The schema of the model
        :param vectorizer: The model for the Vectorizer
        :param models: A list of machine learning models
        """
        self.context = context
        self.schema = schema
        self.vectmodel = vectorizer
        self.models = MODELS

    def _predictAction(self, test=False):
        """
        Compute a predict for the object
        """
        line = '\n\n' + 30 * '-' + '\n'

        # Validate parametres
        errors = self._validate_schema()
        if errors:
            return errors

        # Get the learning adapter for object
        obj_learning = ILearningString(self.context)

        # Get the vectorizer
        obj_vector = self.vectmodel(self.context, self.schema)
        vectorizer = obj_vector.get_vectorizer()
        # Get the corpus for the object
        text = obj_learning.learningString()
        status = 'Learning string:\n' + text + line
        corpus = vectorizer.transform([text])

        # Predict with the machine learning models
        for model in self.models:
            obj_model = model(self.context, self.schema)
            if test:
                status += obj_model.test_predict(vectorizer, corpus) + line
            else:
                result = obj_model.predict(corpus)[0]
                # Set predicted result
                obj_model.persist_result(self.context, result)

        return status

    def test_predict(self):
        status = self._predictAction(test=True)
        return 'Predicting. ' + status

    def compute_predict(self):
        self._predictAction()

    def _validate_schema(self):
        """
        Check the parametres of the schema.
        Returns None when parametres are correct.
        Returns an error string otherwise
        """
        filepath = os.path.join(
            self.schema.modelsDir, self.schema.clusteringFile)
        if not os.path.exists(filepath):
            return 'Clustering model file does not exist {}'.format(filepath)
        return
