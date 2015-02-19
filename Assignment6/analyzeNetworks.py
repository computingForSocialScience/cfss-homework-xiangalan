import pandas as pd
import numpy as np
import networkx as nx

def readEdgeList(filename):
	data = pd.read_csv(filename)
	
	#return data
#print readEdgeList("out_file.csv")
	if len(data.columns) > 2:
		print "Warning! Csv has more than two columns"
		data = pd.read_csv(filename, usecols=[0, 1])
		dataframe =pd.DataFrame(data)
	else:
		dataframe = pd.DataFrame(data)
	#print dataframe
	return dataframe

#print readEdgeList("out_file.csv")	




def degree(edgeList, in_or_out):
	if in_or_out == "in":
		degree = edgeList['1'].value_counts()
	if in_or_out == "out":
		degree = edgeList['0'].value_counts()
	return degree
#print degree("out_file.csv", "in")

in_or_out = 'out'
filename = 'out_file.csv'
edgeList = readEdgeList(filename)
#print degree(edgeList, in_or_out)



def combineEdgeLists(edgeList1, edgeList2):
	concatenated = pd.concat([edgeList1,edgeList2])
	#print concatenated.drop_duplicates()
	return concatenated.drop_duplicates()

#combineEdgeLists(readEdgeList('out_file.csv'),readEdgeList('out_file2.csv'))



def pandasToNetworkX(edgeList):
	g = nx.DiGraph()
	for sender,receiver in edgeList.to_records(index=False):
		g.add_edge(sender,receiver)
	return(g)
#pandasToNetworkX(readEdgeList('out_file.csv'))



def randomCentralNode(inputDiGraph):
	centrality_dict = nx.eigenvector_centrality(inputDiGraph)
	normalization = sum(centrality_dict.values())
	for key in centrality_dict:
		try:
			centrality_dict[key] = centrality_dict[key]/float(normalization)
		except ZeroDivisionError:
			centrality_dict[key] = 1.0/len(centrality_dict)
	random_node = np.random.choice(centrality_dict.keys(), p=centrality_dict.values())
	return random_node

#randomCentralNode(pandasToNetworkX(combineEdgeLists(readEdgeList('out_file.csv'),readEdgeList('out_file2.csv'))))
