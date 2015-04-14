from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.learning.settings import ISettings
from plone.app.learning.interfaces import ILearningUpdate



def cluster_info(ncluster, context):
		catalog = getToolByName(context, 'portal_catalog')

		registry = getUtility(IRegistry)
		schema = registry.forInterface(ISettings)

		return { 
				'number': ncluster, 
				'elements': catalog(MachineLearningCluster=ncluster), 
				'topwords': ', '.join(schema.clustersTerms.get(ncluster,'')),
				}


class AutoSitemapView(BrowserView):
    """
    View for the Autositemap. Very much like the sitemap view but this is automatically learned.

    :iparam context: IPloneSiteRoot
    """
    def clustering_map(self):
		catalog = getToolByName(self.context, 'portal_catalog')
		indexed_cluster = catalog.Indexes['MachineLearningCluster']

		return [ cluster_info(key, self.context)
			for key in indexed_cluster.uniqueValues()]
			

class AutoLearnedViewlet(ViewletBase):
	def clustering(self):
		clustergroup = ILearningUpdate(self.context).getClusterGroup()
		info = cluster_info(clustergroup, self.context)

		this_path = '/'.join(self.context.getPhysicalPath())
		info['elements'] = filter(lambda br: br.getPath() != this_path ,  info['elements'])
		return info


