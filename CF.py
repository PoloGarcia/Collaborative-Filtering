import scipy as sc
import numpy as np
import heapq
import dominate
from dominate.tags import *
import collections

np.set_printoptions(threshold=np.nan)

def parser(filename, separator):
    print 'Building rating records...'
    fileobj = open(filename, 'r')
    lines = fileobj.readlines()[0:]
    dicData = {}
    itemIdSet = set()
    sparseMatrix = []

    for line in lines:
            data = line.rstrip().replace('"','').split(separator)
            itemIdSet.add(data[1])
            if data[0] not in dicData.keys():
                dicData[data[0]] = {}
                dicData[data[0]][data[1]] = int(data[2])
            else: 
                dicData[data[0]][data[1]] = int(data[2])

    itemIdSet = list(itemIdSet)
    users = dicData.keys()
    for user in dicData.keys():
        row = []
        for isbn in itemIdSet:
            if isbn in dicData[user].keys():
                row.append(dicData[user][isbn])
            else:
                row.append(0)
        sparseMatrix.append(row)

    sparseMatrix = np.array(sparseMatrix)

    fileobj.close()
    print 'done'

    return sparseMatrix,users,itemIdSet,dicData

def build_preferences(sparseMatrix):
    print 'Building preference matrix...'
    tSparseMatrix = sparseMatrix.transpose()
    preferenceMatrix = np.dot(tSparseMatrix, sparseMatrix)
    print 'done'

    return preferenceMatrix

def c_filter(user, users, sm, pm):
    print 'Filtering...'
    user_index = users.index(user)
    user_preferences = sm[user_index]
    user_recommendations = np.dot(pm, user_preferences)
    print 'done'

    return user_preferences, user_recommendations

def recommend(user, up, ur, dataSet, items, top_n):
    print 'Building top recommendations...'
    #get user watched movies
    for movie in dataSet[user].keys():
        ur[items.index(movie)] = 0  #discard already watched movies
    print 'done'

    indexes = heapq.nlargest(top_n, range(len(ur)), ur.take)

    values = []
    for index in indexes:
        values.append(ur[index])

    return indexes,values

def buildHTML(user,indexes,dicItems,itemIdSet,dataSet,values):
    print 'Building html output'
    doc = dominate.document(title='Top recommendations for ' + str(user))
    sortedData = sorted(dataSet[str(user)].items(),key=lambda x: x[1],reverse=True) 
    with doc.head:
        link(rel='stylesheet', href='http://cdn.foundation5.zurb.com/foundation.css')

    with doc:
        with div(id='header', cls='small-7 large-centered columns'):
            h1('recommendations for user ' + str(user))
        with div(id='content', cls='small-7 large-centered columns'):
            h3('We recommend:')
            with table().add(tbody()):
                l = tr()
                l.add(th('Place'))
                l.add(th('Title'))
                l.add(th('Genre'))
                l.add(th('Recommendator value'))
                for counter, index in enumerate(indexes):
                    itemId = itemIdSet[index]
                    l = tr()
                    l.add(td(str(counter+1)))
                    l.add(td(a(dicItems[itemId]['name'],href=dicItems[itemId]['url'])))
                    l.add(td(dicItems[itemId]['genre']))
                    l.add(td(values[counter]))

            h3('You have seen:')
            with table().add(tbody()):
                l = tr()
                l.add(th('Title'))
                l.add(th('Rating'))
                l.add(th('Genre'))
                for (movie,rating) in sortedData:
                    l = tr()
                    l.add(td(a(dicItems[movie]['name'],href=dicItems[movie]['url'])))
                    l.add(td(dataSet[str(user)][movie]))
                    l.add(td(dicItems[movie]['genre']))

    f = open('output.html','w+')
    f.write(str(doc))
    f.close()

    print 'done'
    return

def buildItems(filename,separator):
    fileobj = open(filename, 'r')
    lines = fileobj.readlines()[0:]
    dicItems = {}

    for line in lines:
        data = line.rstrip().replace('"','').split(separator)
        dicItems[data[0]] = {}
        dicItems[data[0]]['name'] = data[1]
        dicItems[data[0]]['url'] = data[4]
        #unknown | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy |Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western | 
        #   5        6          7           8           9          10       11        12          13       14        15         16      17        18        19        20        21      22      23
        genreList = data[5:]
        genre = genreList.index('1')+5
        genres = { 5:'unknown', 6:'Action', 7:'Adventure', 8:'Animation', 9:'Children\'s', 10:'Comedy', 11:'Crime', 12:'Documentary', 13:'Drama', 14:'Fantasy', 15:'Film-Noir', 16:'Horror', 17:'Musical', 18:'Mystery', 19:'Romance', 20:'Sci-Fi', 21:'Thriller', 22:'War', 23:'Western'}
        dicItems[data[0]]['genre'] = genres[genre]
    return dicItems

dicItems = buildItems('./ml-100k/u.item','|')
sparseMatrix,users,itemIdSet,dataSet = parser('./ml-100k/u.data','\t') #TODO change for actual input
#sparseMatrix = value[0]
#users = value[1]
#itemIdSet = value [3]
preferenceMatrix = build_preferences(sparseMatrix)
user_arrays = c_filter("6", users, sparseMatrix, preferenceMatrix)
indexes,values = recommend("6", user_arrays[0], user_arrays[1], dataSet, itemIdSet, 10)
buildHTML(6,indexes,dicItems,itemIdSet,dataSet,values)


