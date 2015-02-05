import csv
import sys
import matplotlib.pyplot as plt

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

def get_avg_latlng(filename):
	lines = readCSV("permits_hydepark.csv")
	sum_lat = 0
	sum_lng = 0
	j = 0
	for i in lines:
		if i[-3] == "":
			j += 1
			continue
		sum_lat += float(i[-3])
		sum_lng += float(i[-2])
	avg_lat = sum_lat/(len(lines)-j)
	avg_lng = sum_lng/(len(lines)-j)
	return avg_lat, avg_lng
print get_avg_latlng("permits_hydepark.csv")

    


def zip_code_barchart(filename):
	lines = readCSV("permits_hydepark.csv")
	zipcode = []
	q = [28,35,42,49,56,63,70,77,84]
	for i in lines:
		for p in q:
			if i[p] != "":
				zipcode.append(int(i[p][:5]))
		
	print zipcode
	plt.hist(zipcode, bins=400)
	plt.title("Zip Codes")
	plt.xlabel("Contractor Zip Code")
	plt.ylabel("Frequency")
	
	plt.savefig("zip_code_fre_distribution.jpg")
	plt.show()
	



if sys.argv[1] == "latlong":
	get_avg_latlng("permits_hydepark.csv")
elif sys.argv[1] == "hist":
	zip_code_barchart("permits_hydepark.csv")
### enter your code below
