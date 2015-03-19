from __future__ import division
import tweepy,json,urllib2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from urllib2 import urlopen
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

pd.options.display.max_columns = 50
pd.options.display.max_rows= 50
pd.options.display.width= 120
mapsApiKey = "AIzaSyApsWQJfuvUm4lQFontN-S7I9cpUvwoudI"
# mapsApiKey = "AIzaSyDlob61-sori7DBNP7HPuhFq5mO6pu3Eqo"
#here is code for getting country from location
#######################################################################################################################
def getTwitterLocationCountry(location):
    if location is None or location == '':
        return 'None'
    try:
        geoCode = getGeoCode(location)
        return geoCode
        result = getCountryFromGeocode(*geoCode)
    except IndexError:
        print 'index error ' + location
        return 'None'
    except urllib2.HTTPError:
        print 'maps api error'
        return 'None   '
    return  result # we pass 'unpacked' tuple

### get latitude and longitude from twitter user location
def getGeoCode(location): # we ask google places for latitude and longitude
    global mapsApiKey
    location = parseQuery(location)
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + location+ '&key=' + mapsApiKey
    v = urlopen(url.encode('utf-8')).read()
    data = json.loads(v)
    print url
    return data['results'][0]['formatted_address'].split(', ')[-1]

def parseQuery(query): #in order to this we need to create valid url
    result = ''
    for character in query:
        if character.isalpha() or character in ['-','_']:
            result = result + character
        else:
            result = result + '+'
    return result

### getting country from lattitude and longitude
def getCountryFromGeocode(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    try :
        components = j['results'][0]['address_components']
    except IndexError:
        return 'None4'

    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return country
#######################################################################################################################

## Authentication
consumer_key = "OtzLM1lsdFBS0qSb1zGehLSTE" # Use your own key. To get a key https://apps.twitter.com/
consumer_secret = "iY8CRZyJhVOibLO1qxe8SInQ1WkG2VTn8zyepSzUEFdUFUviWU"

consumer_key = "mj8DQXTO1DH30vyZBPfMsze3r" # Use your own key. To get a key https://apps.twitter.com/
consumer_secret = "OozYtXVWOYeLBPqhoh8OvxdxU8iFC2Na743SgTVpHUHonmOsoz"

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

api = tweepy.API(auth)

results = api.search(q="#Democracy")


#### Using Cursor for Pagination


results = []
try:
    for tweet in tweepy.Cursor(api.search, q="#Democracy").items(100):
        results.append(tweet)
except Exception:
    print Exception
    pass

print len(results)
counter =0
usa_counter = 0
india_counter = 0
##################################################
#### Store Results in a Data Frame
def process_results(results):
    id_list = [tweet.id for tweet in results if filterTweet(tweet)]
    data_set = pd.DataFrame(id_list, columns=["id"])
    # Processing Tweet Data

    data_set["text"] = [tweet.text for tweet in results if filterTweet(tweet)]
    data_set['filtered_words'] = [getTweetWords(tweet.text) for tweet in results if filterTweet(tweet)]

    data_set["created_at"] = [tweet.created_at for tweet in results if filterTweet(tweet)]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results if filterTweet(tweet)]
    data_set["favorite_count"] = [tweet.favorite_count for tweet in results if filterTweet(tweet)]
    data_set["source"] = [tweet.source for tweet in results if filterTweet(tweet)]
    # Processing User Dat if filterTweet(tweeta
    data_set["user_id"] = [tweet.author.id for tweet in results if filterTweet(tweet)]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results if filterTweet(tweet)]
    data_set["user_name"] = [tweet.author.name for tweet in results if filterTweet(tweet)]
    data_set["user_created_at"] = [tweet.author.created_at for tweet in results if filterTweet(tweet)]
    data_set["user_description"] = [tweet.author.description for tweet in results if filterTweet(tweet)]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results if filterTweet(tweet)]
    data_set["user_friends_count"] = [tweet.author.friends_count for tweet in results if filterTweet(tweet)]
    data_set["user_location"] = [tweet.author.location for tweet in results if filterTweet(tweet)]
    data_set['user_country'] = [getTwitterLocationCountry(tweet.author.location) for tweet in results if filterTweet(tweet)]
    data_set.sort(['user_country'])

    usa_tweets = 0
    country_word_bag = {}
    country_tweet_count = {}
    country_total_words = {}
    country_probalities = {}
    global usa_counter
    usa_counter = len([x for x in data_set['user_country'] if x=='USA'])
    global india_counter
    india_counter = len([x for x in data_set['user_country'] if x=='India'])
    for country in data_set['user_country']:
        try:
            country_word_bag[country]
        except KeyError:
            country_word_bag[country] = {}
        try:
            country_probalities[country]
        except KeyError:
            country_probalities[country] = {}

    election_x = []
    election_y = []
    water_x = []
    water_y = []

    print usa_tweets
    for i in range(len(data_set['user_country'])):
        country = data_set['user_country'][i]
        if country == 'None' and country not in ['India','USA']:
            continue
        try:
            country_tweet_count.update({country : country_tweet_count[country] +1})
        except KeyError:
            country_tweet_count.update({country : 1})
        try:
            country_total_words[country] += len(data_set['filtered_words'][i])
        except KeyError:
            country_total_words[country] = len(data_set['filtered_words'][i])
        except TypeError:
            continue


        for word in data_set['filtered_words'][i]:
            try:
                country_word_bag[country].update({word : country_word_bag[country][word] + 1})
            except KeyError:
                country_word_bag[country].update({word : 1})

        if country == 'USA':
            country = 0
            if usa_tweets == india_counter:
                continue
            else :
                usa_tweets +=1
        elif  country == 'India':
            country = 1
        else:
            continue

        election = 0
        water = 0

        # exit()
        for word in data_set['filtered_words'][i]:
            if word in ['election','voting', 'campaign']:
                election += 1
            if word in ['electricity', 'wifi', 'water', 'toilet' ,'sanitation']:
                water += 1

        election_x.append(election)
        election_y.append(country)
        water_x.append(water)
        water_y.append(country)
    import pprint
    # pprint.pprint(election_x)
    # exit()
    global counter
    for country in data_set['user_country']:
        if country == 'None' and country not in ['India','USA']:
            counter+=1
            continue
        for word in country_word_bag[country]:
            country_probalities[country][word] = country_word_bag[country][word]/country_total_words[country]
    ###################################
    # save country data to csv
    #save word
    import csv
    with open('countries_words.csv', 'wb') as csvfile:
        country_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        country_writer.writerow(['country']  + ['word'] + ['word_count']+['probability'])
        for country in country_tweet_count:
            if country not in ['India','USA','States']:
                continue
            for word in reversed(sorted(country_word_bag[country], key=country_word_bag[country].get)):
                # if unicode(word,'utf-8').strip() == word:
                word.encode('utf-8').strip()
                country_writer.writerow([country]+ [word.encode('utf-8').strip()] +[country_word_bag[country][word]]+ [country_probalities[country][word]])

    #india
    import csv
    with open('india.csv', 'wb') as csvfile:
        country_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        country_writer.writerow(['word'] + ['ranking']+['word count']+['probability'])
        important_words = ['electricity', 'wifi', 'clean water', 'toilet', 'prosperity', 'election', 'voting', 'campaign']
        for country in country_tweet_count:
            if country != 'India':
                continue
            ranking = 0
            for word in reversed(sorted(country_word_bag[country], key=country_word_bag[country].get)):
                ranking +=1
                if word in important_words:
                    country_writer.writerow([unicode(word).encode('utf-8').strip()] +[ranking]+[country_word_bag[country][word]] + [country_probalities[country][word]])

            for word in important_words:
                try:
                    country_word_bag[country][word]
                except:
                    country_writer.writerow([unicode(word).encode('utf-8').strip()] +[ranking]+[0] + [0])

    #######################################
    # usa

    with open('usa.csv', 'wb') as csvfile:
        country_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        country_writer.writerow(['word'] + ['ranking']+['word count']+['probability'])
        important_words = ['electricity','wifi', 'clean water', 'toilet', 'prosperity', 'election', 'voting', 'campaign']
        for country in country_tweet_count:
            if country != 'USA':
                continue
            ranking = 0
            for word in reversed(sorted(country_word_bag[country], key=country_word_bag[country].get)):
                ranking +=1
                if word in important_words:
                    country_writer.writerow([unicode(word).encode('utf-8').strip()] +[ranking]+[country_word_bag[country][word]] + [country_probalities[country][word]])

            for word in important_words:
                try:
                    country_word_bag[country][word]
                except:
                    country_writer.writerow([unicode(word).encode('utf-8').strip()] +[ranking]+[0] + [0])

    with open('usa_ranking.csv', 'wb') as csvfile:
        country_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        country_writer.writerow(['ranking']+['word'] +['word count']+['probability'])
        for country in country_tweet_count:
            if country != 'USA':
                continue
            ranking = 0
            for word in reversed(sorted(country_word_bag[country], key=country_word_bag[country].get)):
                ranking +=1
                country_writer.writerow([ranking]+ [unicode(word).encode('utf-8').strip()] +[country_word_bag[country][word]] + [country_probalities[country][word]])

    with open('india_ranking.csv', 'wb') as csvfile:
        country_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        country_writer.writerow(['ranking']+['word'] +['word count']+['probability'])
        for country in country_tweet_count:
            if country != 'India':
                continue
            ranking = 0
            for word in reversed(sorted(country_word_bag[country], key=country_word_bag[country].get)):
                ranking +=1
                country_writer.writerow([ranking]+ [unicode(word).encode('utf-8').strip()] +[country_word_bag[country][word]] + [country_probalities[country][word]])

    #regression
    linear_regression(election_x,election_y)
    linear_regression(water_x,water_y)
    return data_set

def filterTweet(tweet):
    return tweet.author.followers_count < 5000

def getTweetWords(text):
    stopWords = stopwords.words('english')
    lmtzr = WordNetLemmatizer()
    filtered_words = [lmtzr.lemmatize(w) for w in text.split() if not w in stopWords]
    return filtered_words
###########################################
# linear regression
def linear_regression(added_up_words,countries):
    from numpy import arange,array,ones#,random,linalg
    from pylab import plot,show
    from scipy import stats

    xi = added_up_words #[0,1,2,0,1,5,1] #added up words
    y =  countries      #[0,1,1,1,1,0,0] #countries

    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)

    print 'r value', r_value
    print  'p_value', p_value
    print 'standard deviation', std_err

    line = [slope*element+intercept for element in xi]
    plot(xi,line,'r-',xi,y,'o')
    show()

########################################################
data_set = process_results(results)
data_set = data_set[data_set['user_country'].isin(['India','USA'])]
data_set.to_csv('data1_7.csv', index=False,encoding = 'utf-8')

print counter
print 'total usa tweets:' + str(usa_counter)
print 'total india tweets' + str(india_counter)