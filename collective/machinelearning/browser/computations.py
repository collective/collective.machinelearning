from Products.Five import BrowserView
from collective.machinelearning.interfaces import ILearningModel, IPredictModel


class ComputeView(BrowserView):
    """
    View for the computeAction

    :iparam context: IPloneSiteRoot
    """
    def __call__(self):
        status = ILearningModel(self.context).compute() 
        return status


class GetLearningView(BrowserView):
    """
    View for the computeAction

    :iparam context: IPloneSiteRoot
    """
    def __call__(self):
        status = ILearningModel(self.context).get_results() 
        return status




class TestPredictView(BrowserView):
    """
    Compute a test predict for the object

    Context is an IMachineLearning object 
    """
    def __call__(self):
        models = IPredictModel(self.context)
        return models.test_predict()


class ComputePredictView(BrowserView):
    """
    Compute a predict for the object

    Context is an IMachineLearning object 
    """
    def __call__(self):
        models = IPredictModel(self.context)
        models.compute_predict()
        return "Predicted and stored"

