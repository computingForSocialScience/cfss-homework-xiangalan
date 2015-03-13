import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = "https://api.spotify.com/v1/artists/" + artist_id + "/albums?offset=0&limit=20&album_type=album&market=US"
    req = requests.get(url)
    data = req.json()
    items_value = data["items"]

    Album_Ids = []
    for i in range(0, len(items_value)):
    	album_id = items_value[i]["id"]
    	Album_Ids.append(album_id)
    return(Album_Ids)

#print fetchAlbumIds("0vYkHhJ48Bs3jWcvZXvOrP")




def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = "https://api.spotify.com/v1/albums/?ids=" + album_id
    req = requests.get(url)
    info1 = req.json()
    info = info1["albums"][0]
    album_info_dict = {}
    album_info_dict['artist_id'] = info['artists'][0]['id']
    album_info_dict['album_id'] = info['id']
    album_info_dict['name'] = info['name']
    album_info_dict['year'] = info['release_date'][:4]
    album_info_dict['popularity'] = info['popularity']
    return(album_info_dict)
#print fetchAlbumInfo("67epO9J9KoY8KSFA4xC4kA")
    
    
    
    
    
    #data = req.json()
    #Album_Info = {}
    #album_value = data["albums"]
    #for i in range(0, len(album_value)):
    	#Album_Info["artist_id"] = album_value[i]["artists"]["id"]
    	#Album_Info["album_id"] = album_value[i]["id"]
    	#Album_Info["name"] = album_value[i]["name"]
    	#year_raw = str(album_value[i]["release_date"]
    	#Album_Info["year"] = year_raw[0:4]
    	#Album_Info["popularity"] = album_value[i]["popularity"]
    #return(Album_Info)
#print fetchAlbumInfo(fetchAlbumIds("0vYkHhJ48Bs3jWcvZXvOrP"))

