import scipy as sc
import numpy as np

def parser(filename):
	fileobj = open(filename, 'r')
	lines = fileobj.readlines()[1:]
	dicData = {}
	isbnSet = set()
	sparseMatrix = []

	for line in lines:
            data = line.rstrip().replace('"','').split(';')
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
				row.append(-1)
		sparseMatrix.append(row)

	sparseMatrix = np.array(sparseMatrix)

	return sparseMatrix,users

value = parser('BX-Book-Ratings-chico.csv') #TODO change for actual input
sparseMatrix = value[0]
users = value[1]
print sparseMatrix
print users
