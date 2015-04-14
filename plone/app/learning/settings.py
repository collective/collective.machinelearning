from zope import schema
from zope.interface import Interface
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from z3c.form import form, group, field, button

#import cProfile

from plone.app.learning.behaviors import IMachineLearning
from plone.app.learning.interfaces import ILearningModel
from plone.app.learning import _


class ISettingsDefault(Interface):
    """ Define settings data structure """

    modelsDir = schema.TextLine(
    	title=u"Filesystem directory storage",
        description=u"Directory to store the models' pickle files"
        )




class ISettingsVectorizer(Interface):


    # useTfidf = schema.Bool(
    #     title=_(u"Tf-IDF"),
    #     description=_(u"Use Tf-IDF in the vectorizer"),
    #     )	

    useNltk = schema.Bool(
       title=_(u"NLTK stem"),
       description=_(u"Use NLTK stem in the vectorizer"),
       )	

    stopWords = schema.TextLine(
       title=_(u"Stop Words"),
       description=_(u"""Words that are too frequent to be considered. 
       	Example: a the for. Defaults: english (stop words for english)"""),  
        )	

    ngramRangeMin = schema.Int(
       title=_(u"Minimum N-gram range of words"),
       description=_(u"""Group words together for the vectorizer. Minimum group size.
      Defaults to 1: only one word"""),   
        )	

    ngramRangeMax = schema.Int(
       title=_(u"Maximum N-gram range of words"),
       description=_(u"""Group words together for the vectorizer. Maximum group size.
       	Defaults to 1: only one word"""),  
        )	

    useRemembering = schema.Bool(
       title=_(u"Remember string<->hashes mapping"),
       description=_(u"Human vocabulary. Slower and more memory consuming."),
       )    



class ISettingsClustering(Interface):

    nClusters = schema.Int(
       title=_(u"Number of clusters"),
       description=_(u"Maximum number of clusters"),   
        ) 

    clusteringFile = schema.TextLine(
       title=_(u"Cluster model file name"),
       description=_(u"The filename that will be stored into directory storage"),  
        )	

    clustersTerms = schema.Dict(
        title=_(u"Top terms per cluster"),
        description=_(u"Learned clusters and top terms for each. Needs Vectorizer remembering."),  
        required=False,
        readonly=True,
        key_type=schema.Int(required=False),
        value_type=schema.List(
            value_type=schema.TextLine(required=False),
            required=False,
            ),
        )




class ISettings(ISettingsDefault, ISettingsVectorizer, ISettingsClustering):
    """
    Unified panel
    """
    pass


class FormVectorizer(group.Group):
    label = _(u"Vectorizer")
    fields = field.Fields(ISettingsVectorizer)

class FormClustering(group.Group):
    label = _(u"Cluster model")
    fields = field.Fields(ISettingsClustering)


class SettingsPanelForm(RegistryEditForm):
    """
    Define form logic
    """
    form.extends(RegistryEditForm)
    schema = ISettings
    fields = field.Fields(ISettingsDefault)
    groups = (FormVectorizer,FormClustering)


    @button.buttonAndHandler(_(u"Compute"), name='compute')
    def handleCompute(self, action):
        model = ILearningModel(self.context)

        #pr = cProfile.Profile()
        #pr.enable()
        self.status = model.compute()
        #pr.create_stats()
        #pr.print_stats(sort='cumtime')




SettingsPanelView = layout.wrap_form(SettingsPanelForm, ControlPanelFormWrapper)
SettingsPanelView.label = _(u"Machine Learning settings")





