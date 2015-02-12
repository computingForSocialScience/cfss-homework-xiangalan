from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """

    url = "https://api.spotify.com/v1/search?q=" + name + "&type=artist"
    req = requests.get(url)
    Data= req.json()
    ID = Data['artists']['items'][0]['id']
    return(ID)

# print fetchArtistId("Patti Smith")

   



def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    artist_info_dict = {}
    url = "https://api.spotify.com/v1/artists/" + artist_id
    req = requests.get(url)
    Data= req.json()
    followers2 = Data['followers']['total']
    genres2 = Data['genres']
    id2 = Data['id']
    name2 = Data['name']
    popularity2 = Data['popularity']
    Info_valuelist = [followers2, genres2, id2, name2, popularity2]
    Info_keys = ["followers", "genres", "id", "name", "popularity"]
    artist_info_dict = dict(zip(Info_keys, Info_valuelist))
    return (artist_info_dict)
#print fetchArtistInfo(fetchArtistId("Patti Smith"))
    	
    
