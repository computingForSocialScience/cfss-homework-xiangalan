import unicodecsv as csv     #import necessary library, which can read csv files containing unicode
import matplotlib.pyplot as plt  #import a library that can plot

def getBarChartData():      #define a function that can get data from csv files
    f_artists = open('artists.csv')   #open two csv files we created before
    f_albums = open('albums.csv')

    artists_rows = csv.reader(f_artists)  #reading csv information by rows and save them to a variable
    albums_rows = csv.reader(f_albums)

    artists_header = artists_rows.next()  #jump to the next line
    albums_header = albums_rows.next()

    artist_names = []   #create a list for artists' names
    
    decades = range(1900,2020, 10)   # create a range of period from 1900 to 2020, with 10 years as interval, in which the album is created
    decade_dict = {}   #create a dictionary for the decade an album was made
    for decade in decades:
        decade_dict[decade] = 0   #set the initial number of album in every decade as 0
    
    for artist_row in artists_rows:   #for every element in artist_rows
        if not artist_row:  #if there is any blank row, skip it
            continue
        artist_id,name,followers, popularity = artist_row   #give values to artist_id,name,followers, popularity from the content of that row
        artist_names.append(name)   #append the value of list to the artist_names list

    for album_row  in albums_rows:    # for every element in albums_rows
        if not album_row:    #if the row is blank, skip it
            continue
        artist_id, album_id, album_name, year, popularity = album_row  #set the values of the variables artist_id, album_id, album_name, year, popularity to be the corresponding values in the row 
        
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):   #if the year of that album falls into the interval (decade,decade+10)
                decade_dict[decade] += 1    # add 1 to the value with the key [decade] in the dictionary
                break

    x_values = decades     #define x_values to be the list decades
    y_values = [decade_dict[d] for d in decades]     #define y_values to be a list of values of decade_dict corresponding to every key in list decades
    return x_values, y_values, artist_names   # let the function return to the value x_values,y_values and artist_names


def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData()   #set x_vals, y_vals and artist_names as the three outputs generated by getBarChartData function
    
    fig , ax = plt.subplots(1,1)   #create a figure and one subplot with 1 row and 1 column
    ax.bar(x_vals, y_vals, width=10)   # set the graph to be a barchart with bar width of 10
    ax.set_xlabel('decades')    #name the x label decades
    ax.set_ylabel('number of albums')   # name the y label number of albums
    ax.set_title('Totals for ' + ', '.join(artist_names))   #name the title of the graph the totals for artists
    plt.show()   # plot the graph

    
