from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
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

#### Using Cursor for Pagination

# For data mining you will be dealing with a large amount of results. Cursor is a simple way to handle interation and results pages.
counter =0
usa_counter = 0
india_counter = 0
##################################################
#### Store Results in a Data Frame
def process_results():
    data_set = pd.DataFrame.from_csv('filtered_data.csv',encoding = 'utf-8')
    # Processing Tweet Data
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
    temp = []
    for x in data_set['filtered_words']:
        temp.append(x)
    print temp[0]
    data_set['filtered_words'] = temp

    print usa_tweets
    for i in range(len(data_set['filtered_words'])):
        try:
            temp[i] = [x[1:] for x in temp[i][:-1].split(',')]
        except TypeError:
            temp[i] = []

    arr = []
    data_set['filtered_words'] = temp
    for country in data_set['user_country']:
        arr.append(country)

    for i in range(len(data_set['user_country'])):
        # try:
        country = arr[i]

        if country == 'None' and country not in ['India','USA']:
            continue
        try:
            country_tweet_count.update({country : country_tweet_count[country] +1})
        except KeyError:
            country_tweet_count.update({country : 1})
        try:
            country_total_words[country] += len(temp[i])
        except KeyError:
            country_total_words[country] = len(temp[i])
        except TypeError:
            continue


        for word in temp[i]:
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
        for word in temp[i]:
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
data_set = process_results()
# data_set.to_csv('data2.csv', index=False,encoding = 'utf-8')

print counter
print 'total usa tweets:' + str(usa_counter)
print 'total india tweets' + str(india_counter)

pd.DataFrame.from_csv('filtered_data.csv')