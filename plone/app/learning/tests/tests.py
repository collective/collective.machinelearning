import unittest

from sklearn.feature_extraction.text import HashingVectorizer

from plone.app.learning.machinelearning.vectorizer import Vectorizer




class MockSchema(object):
	useNltk = False
	stopWords = 'english'
	ngramRangeMin = 1
	ngramRangeMax = 2
	useRemembering = False



class TestProgramUnit(unittest.TestCase):
    """
    Unit test for the Program type
    """

    def test_get_vectorizer(self):
    	context = None
    	schema = MockSchema()

    	vect_obj = Vectorizer(context, schema)
    	vectorizer = vect_obj.get_vectorizer()

    	self.assertIsInstance(vectorizer, HashingVectorizer)




def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)