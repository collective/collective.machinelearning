

from sklearn.cluster import KMeans



def clustering_model(corpus,n_clusters=50):
	nsamples = corpus.shape[0]
	nclusters = min(n_clusters, nsamples/2) #restrict n for few documents

	km = KMeans(n_clusters=nclusters, init='random', n_init=1)
	km.fit(corpus)

	return km


def clustering_top_terms(model,vectorizer):
	"""
	Top terms per cluster
	"""
	TOP = 10
	order_centroids = model.cluster_centers_.argsort()[:, ::-1]
	size = order_centroids.shape[0]
	terms = vectorizer.get_feature_names()

	clusterdict = {}
	for i in range(size):
		clusterdict[i] = [ terms[t] for t in order_centroids[i, :TOP] if t in terms ]

	return clusterdict


