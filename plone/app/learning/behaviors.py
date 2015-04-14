"""
Behaviours for Machine Learning.
"""
from zope import schema
from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from plone.app.learning import _


class IMachineLearning(model.Schema):
    """
    Behavior interface to make a Dexterity type support Machine Learning 
    """
    model.fieldset('machinelearning',
            label=_(u"Learning"),
            fields=['machineLearningCluster',]
        )
    
    machineLearningCluster = schema.Int(
        title=_(u'label_machine_learning_cluster', default=u'Related cluster'),
        required=False,
        )

   
alsoProvides(IMachineLearning, IFormFieldProvider)
