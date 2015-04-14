
"Utilities for machine learning"

import pickle
import os.path


#Serialization

def save_model(model,directory,name):
	f = open(os.path.join(directory,name),'w')
	pickle.dump(model,f)
	f.close()


def load_model(directory,name):
	f = open(os.path.join(directory,name),'r')
	return pickle.load(f)

