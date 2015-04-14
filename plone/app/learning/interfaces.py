from zope.interface import Interface

# Machine learning interfaces
class ILearningString(Interface):
    """
    Interface for objects providing a string for machine learning
    """
    def learningString(self):
        """
        Returns a string.
        """
        pass

    def learningTags(self):
        """
        Returns a collection of strings or ('unknown', ) if empty
        """
        pass


class ILearningUpdate(Interface):
    """
    Interface for objects updatable with learning results
    """    
    def setClusterGroup(self,group):
        pass
    def getClusterGroup(self):
        pass





# Model computations interfaces
class ILearningModel(Interface):
    """
    Interface for objects providing a Machine Learning model learning
    """
    def compute(self):
        """
        Compute the model
        """
        pass


class IPredictModel(Interface):
    """
    Interface for objects providing a Machine Learning model prediction
    """ 
    def test_predict(self):
        """
        Returns a test prediction
        """
        pass

    def compute_predict(self):
        """
        Returns a test prediction
        """
        pass

