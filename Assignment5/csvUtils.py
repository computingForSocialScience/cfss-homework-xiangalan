from io import open
from fetchArtist import *
from fetchAlbums import *

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f = open('artist.csv','w')
    f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    
    for artist_info_dict in artist_info_list:
    	f.write('"' + artist_info_dict['id'] + '","' + artist_info_dict['name'] + '",' + str(artist_info_dict['followers']) + ',' + str(artist_info_dict['popularity']) + '\n')
    f.close()
#writeArtistsTable(fetchArtistInfo(fetchArtistId("Patti Smith")))   did not turn into a list
#writeArtistsTable([fetchArtistInfo(fetchArtistId("Patti Smith"))])   turned into a list
 
 
 
   
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    f = open('albums.csv','w')
    f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    
    for album_info_dict in album_info_list:
    	f.write('"' + album_info_dict['artist_id'] + '","' + album_info_dict['album_id'] + '","' + album_info_dict['name'] + '",' + str(album_info_dict['year']) + ',' + str(album_info_dict['popularity']) + '\n')
    f.close()

#album_info_dict = fetchAlbumInfo("67epO9J9KoY8KSFA4xC4kA")

#print album_info_dict['artist_id']

#writeAlbumsTable([fetchAlbumInfo("67epO9J9KoY8KSFA4xC4kA")])
