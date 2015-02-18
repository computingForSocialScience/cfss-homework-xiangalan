import requests

import pandas as pd
import numpy as np


def getRelatedArtists(artistID):
	url = "https://api.spotify.com/v1/artists/" +artistID+ "/related-artists"
	req = requests.get(url)
	Data = req.json()
	RelatedArtists = []
	for i in range(20):
		RelatedArtist = Data["artists"][i]["id"]
		RelatedArtists.append(RelatedArtist)
	return(RelatedArtists)
# print getRelatedArtists("2mAFHYBasVVtMekMUkRO9g")
	
	
	

def getDepthEdges(artistID, depth):
	Edgeslist = []
	list1 = [artistID]
	list2 = []
	while depth != 0:
		for i in list1:
			list2 = getRelatedArtists(i)
			for j in list2:
				tuple = (i,j)
				Edgeslist.append(tuple)
		depth = depth - 1
		if depth == 0:
			break
		list1 = list2
	#return(Edgeslist)
#print getDepthEdges("2mAFHYBasVVtMekMUkRO9g", 2)
	Edgeslist2 = []
	for i in Edgeslist:
		if i not in Edgeslist2:
			Edgeslist2.append(i)
	return Edgeslist2
#print getDepthEdges("2mAFHYBasVVtMekMUkRO9g", 2)




def getEdgeList(artistID, depth):
	"""s = getDepthEdges(artistID, depth)
	for i in s:
		libraries = [i[0],i[1]]
		libraries.append(libraries)
	lib_df = pd.DataFrame(libraries)
	return lib_df
print getEdgeList("2mAFHYBasVVtMekMUkRO9g", 2)"""
	lib_df = pd.DataFrame(getDepthEdges(artistID, depth))
	return lib_df
#print getEdgeList("2mAFHYBasVVtMekMUkRO9g", 2)


def writeEdgeList(artistID, depth, filename):
	data = getEdgeList(artistID, depth)
	data.to_csv(filename, index=False)
	return data

writeEdgeList("2mAFHYBasVVtMekMUkRO9g", 2, "out_file.csv")	
		