Introduction
============



Installation 
============

(be patient as numpy and scipy are large)

1. gfortran is needed, install it into system.

2. Install numpy manually. With pip as with easy_install fails.

3. Run bin/buildout: scipy, nltk and scikit-learn will be installed.


Alternatively, you can use the provided docker development environment:
- make docker-build
- make docker-run
- make
- bin/instance fg




Quick Doc
=========


1. Activate the behavior Machine Learning for dexterity types that you want to be machine learned. If you have content you might reindex object_provides catalog index in order to mark the content correctly.

2. Compute models; that is learning from the data. Two options:

	* From the Compute button in the control panel
	* From the view /computeMachineLearning (useful to combine with cron)

3. See the clusters at /autositemap

4. When adding or modifying content then a prediction can be computed with the view <content>/compute_predict. Prediction can also be tested for a content in the view <content>/test_predict. 
However, models have to be recomputed (step 2) periodically to correctly learn from all contents.






Machine Learning configuration
==============================


Two steps when computing:

1. Vectorizer: text -> vector
2. Model: vector -> model/prediction



In order to have the models for prediciton we need to store them. Now they are stored in a Filesystem directory storage, by default at `var/instance/`.




Vectorizer
----------

* NLTK stem: uses stems of words (only for english). Example: 'dog dogs' -> dog

* Stop words: no use these words for learning as they are too much common.

* N-gram: to learn from groups of words, Example (min=1 max=2): 'a text' -> ('a', 'text', 'a text')

* Remember string/hashes mapping: remebers hash mapping to human vocabulary so then models can give information with human vocabulary. Only for the models' learning step, as the vocabulary mapping is not stored.



Clustering model
----------------

* Number of clusters: defaults to 50. It is a maximum: if there are less than 50 contents then there are less clusters.

* Top words: shows the most important words used when learning for each cluster. It needs the Vectorizer remebering option.





ToDo
====

* Scale machine learning computation and performance analysis: http://scikit-learn.org/stable/modules/scaling_strategies.html
