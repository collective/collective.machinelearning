from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.component import adapts, getUtility
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.registry.interfaces import IRegistry
from plone.app.uuid.utils import uuidToCatalogBrain

from plone.app.learning.interfaces import (
    ILearningString, ILearningUpdate,
    ILearningModel, IPredictModel
)
from plone.app.learning.machinelearning.computations import Predict, Learning
from plone.app.learning.behaviors import IMachineLearning
from plone.app.learning.settings import ISettings


# adapters for Model computations

class MachineLearningModel(Learning):

    """
    Computes learning for objects with IMachineLearning

    :iparam context: The MachineLearning object
    :iparam schema: Is the schema with model fields
    """
    implements(ILearningModel)
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        registry = getUtility(IRegistry)
        schema = registry.forInterface(ISettings)
        super(MachineLearningModel, self).__init__(context, schema)


class MachinePredictModel(Predict):

    """
    Computes predicts for objects with IMachineLearning

    :iparam context: The MachineLearning object
    :iparam schema: Is the schema with model fields
    """
    implements(IPredictModel)
    adapts(IMachineLearning)

    def __init__(self, context):
        registry = getUtility(IRegistry)
        schema = registry.forInterface(ISettings)
        super(MachinePredictModel, self).__init__(context, schema)


# Example adapters for IlearningString

class ContentLearningString(object):

    """
    Adapter for Dexterity Content objects to interface ILearningString
    """
    implements(ILearningString)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def learningString(self):
        # text contained in SearcheableText
        catalog = getToolByName(self.context, 'portal_catalog')
        brain = uuidToCatalogBrain(self.context.UID())
        rid = brain.getRID()
        data = catalog.getIndexDataForRID(rid)
        return ' '.join(data['SearchableText'])

    def learningTags(self):
        tags = self.context.subject
        if tags:
            return tags
        return ('unknown',)


class ContentLearningUpdate(object):

    """
    Adapter for Dexterity Content objects to interface ILearningUpdate
    """
    implements(ILearningUpdate)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def setClusterGroup(self, group):
        self.context.machineLearningCluster = group
        self.context.reindexObject(idxs=["MachineLearningCluster"])

    def getClusterGroup(self):
        return self.context.machineLearningCluster
