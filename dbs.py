from pyrplidar import PyRPlidar
import time
import button
import os
import pickle
from math import sin,cos,pi
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

    
if __name__ == "__main__":
		
	with open('two_people.pkl', 'rb') as f:
		coordinates = pickle.load(f)
		
	#with open('one_person.pkl', 'rb') as f:
	#	coordinates = pickle.load(f)
		
	X = np.array(coordinates)
	X = StandardScaler().fit_transform(X)
	
	dbscan = DBSCAN(eps = 0.35,min_samples = 3)
	labels = dbscan.fit_predict(X)

	print(max(labels))
#	person_one = X[labels == 2]
#	one_size = int(len(person_one))
#	one_center = np.mean(person_one, axis = 0)
#
#	person_two = X[labels == 5]
#	two_size = int(len(person_two))	
	
	
	#print(one_size)
	#print(one_center)
	#print(two_size)
	
#	plt.scatter(X[labels == 0,0], X[labels == 0,1], s = 5, c = "black")
#	plt.scatter(X[labels == 1,0], X[labels == 1,1], s = 5, c = "black")
#	plt.scatter(X[labels == 2,0], X[labels == 2,1], s = 5, c = "green")
#	plt.scatter(X[labels == 3,0], X[labels == 3,1], s = 5, c = "black")
#	plt.scatter(X[labels == 4,0], X[labels == 4,1], s = 5, c = "black")
#	plt.scatter(X[labels == 5,0], X[labels == 5,1], s = 5, c = "blue")
#	plt.scatter(X[labels == 6,0], X[labels == 6,1], s = 5, c = "black")	
#	plt.scatter(X[labels == 7,0], X[labels == 7,1], s = 5, c = "black")
#	plt.scatter(X[labels == 8,0], X[labels == 8,1], s = 5, c = "black")
#	plt.scatter(X[labels == 9,0], X[labels == 9,1], s = 5, c = "black" )
					
#	plt.show()
	
	
	
	
