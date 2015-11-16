import scipy as sc
import numpy as np
import heapq

np.set_printoptions(threshold=np.nan)

def parser(filename, separator):
	fileobj = open(filename, 'r')
	lines = fileobj.readlines()[1:]
	dicData = {}
	isbnSet = set()
	sparseMatrix = []

	for line in lines:
            data = line.rstrip().replace('"','').split(separator)
            isbnSet.add(data[1])
            if data[0] not in dicData.keys():
            	dicData[data[0]] = {}
            	dicData[data[0]][data[1]] = int(data[2])
            else: 
            	dicData[data[0]][data[1]] = int(data[2])

	isbnSet = list(isbnSet)
	users = dicData.keys()
	for user in dicData.keys():
		row = []
		for isbn in isbnSet:
			if isbn in dicData[user].keys():
				row.append(dicData[user][isbn])
			else:
				row.append(0)
		sparseMatrix.append(row)

	sparseMatrix = np.array(sparseMatrix)

	return sparseMatrix,users

def build_preferences(sparseMatrix):
	tSparseMatrix = sparseMatrix.transpose()
	preferenceMatrix = np.dot(tSparseMatrix, sparseMatrix)

	return preferenceMatrix

def c_filter(user, users, sm, pm):
	user_index = users.index(user)
	user_preferences = sm[user_index]
	user_recommendations = np.dot(pm, user_preferences)

	return user_preferences, user_recommendations

def recommend(user, up, ur, top_n):
	return heapq.nlargest(top_n, range(len(ur)), ur.take)


value = parser('./ml-100k/u.data','\t') #TODO change for actual input
print 'done'
sparseMatrix = value[0]
users = value[1]
preferenceMatrix = build_preferences(sparseMatrix)
print 'done'
user_arrays = c_filter("6", users, sparseMatrix, preferenceMatrix)
indexes = recommend("6", user_arrays[0], user_arrays[1], 3)

