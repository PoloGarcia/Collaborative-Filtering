import scipy as sc
import numpy as np

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

def asd(user, users, sm, pm):
	user_index = users.index(user)
	user_preferences = sm[user_index]
	user_recommendations = np.dot(pm, user_preferences)

	print user_preferences
	print user_recommendations


value = parser('./ml-100k/u.data','\t') #TODO change for actual input
print 'done'
sparseMatrix = value[0]
users = value[1]
preferenceMatrix = build_preferences(sparseMatrix)
print 'done'
asd("6", users, sparseMatrix, preferenceMatrix)

