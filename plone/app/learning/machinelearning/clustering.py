from Products.CMFCore.utils import getToolByName
from plone.app.learning.behaviors import IMachineLearning
from plone.app.learning.interfaces import ILearningString, ILearningUpdate
from plone.app.learning.machinelearning.utils.base import CatalogEmpty
from plone.app.learning.machinelearning.utils.persistence import save_model, load_model
from plone.app.learning.machinelearning.utils.vectorizers import nearers
from plone.app.learning.machinelearning.utils.clustering import (
		clustering_model, clustering_top_terms
		)



class Clustering(object):
    """
    Computes clustering for objects with IClustering schema

    :iparam context: Any object (for obtaining portal_catalog, etc.)
    :iparam schema: An abb.learning.settings.ISettings registry proxy
    :iparam learned_objs: The list of objects learned (by order of learning)
    """

    def __init__(self,context, schema):
        self.context = context
        self.schema = schema
        self.learned_objs = []
        self.objects_labels = []

    def compute(self,vectorizer, corpus, persist=False):
    	model = clustering_model(corpus,n_clusters=self.schema.nClusters)
    	#Parametres del model
    	nclust, nfeatures = model.cluster_centers_.shape

    	#Refresh cluster objects
    	self.objects_labels = model.labels_

        #store model
        if persist:
            self._persist_model(model)
            self._update_topterms(model,vectorizer)

     	r = "Clustering. Clusters: {0}"
    	return r.format(nclust)


    def get_results(self):
        return self.objects_labels

    def persist_result(self, content, label):
        ILearningUpdate(content).setClusterGroup(label)


    def predict(self, corpus):
        model = load_model(self.schema.modelsDir,self.schema.clusteringFile)
        return model.predict(corpus)

    def test_predict(self, vectorizer,corpus):
        clustid = self.predict(corpus)[0]

        nears = self._nearers_catalog(vectorizer, corpus, clustid)

        r = "RelatedObjects with clustering predict\n Cluster id: {0}\n Related distance: {1}"
        return r.format(clustid,nears)

    def _persist_model(self,model):
    	#Model pickle
        save_model(model,self.schema.modelsDir,self.schema.clusteringFile)
        
 


    def _update_topterms(self,model,vectorizer):
        #If not cheked remembering, there is no human vocabulary
        if self.schema.useRemembering:
            self.schema.clustersTerms = clustering_top_terms(model,vectorizer)


    def _iterator_catalog_related_objects(self,clustid):
        catalog = getToolByName(self.context, 'portal_catalog')
        related = catalog({
            'object_provides': IMachineLearning.__identifier__,
            'MachineLearning-ClusterGroup': str(clustid) })

        if not related:
            raise CatalogEmpty('Empty catalog: a Computation must be run')

        for ob in related:
            obj = ob.getObject()
            text = ILearningString(obj).learningString()
  
            self.learned_objs.append(obj)
            yield text



    def _nearers_catalog(self,vectorizer,text,clustid):
        try:
            relatedcorpus =  self._iterator_catalog_related_objects(clustid)
            corpus = vectorizer.transform(relatedcorpus)
        except CatalogEmpty:
            return []

        nears = nearers(text,corpus)
        ordered = [ (dist,self.learned_objs[num])  for dist,num in sorted(nears) ]

        return ordered


