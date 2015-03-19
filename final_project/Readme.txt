Idea Origin

The term monitory democracy is introduced in Keane's The Life and Death of Democracy (2009). It claims that from around 1945 democracy entered a new historical phase. In the age of 'monitory democracy', the language and ideals and institutions of democracy undergo many changes. For the first time in its history, democracy has grown familiar to people living within most regions of the earth, regardless of their language, nationality, religion or civilisation. This process of 'indigenisation' helps explain why, again for the first time, there is an explosion of many different understandings of democracy (for many people, especially in poorer countries, it becomes synonymous with justice, electricity, sanitation and other public goods); and why there are references to 'global democracy' and much talk of democracy as a universal ideal. Democracy becomes globally accepted as the political governing form par excellence. For the first time as well, racial prejudice is said to be incompatible with the ideals of democracy. In contrast to the age of representative democracy, which ended just prior to World War Two, many democrats consequently feel embarrassed or angered by talk of 'naturally inferior', or 'backward' or 'uncivilised' peoples.


Three Steps to Finish This Project and Some Notes:

1.	Create a filtered_data csv file, with 10000 tweets from India and 10000 tweets from the US with “# democracy” in tweet text. (Google API is used to scrape data exactly from these two places). User location column should not be empty, and it should be India/US or cities in these countries. It could be India.csv file as below. Note the highlighted user_location column.

2.	Based on the filtered_data csv file above, using NLTK to tokenize tweet text (in text column), eliminate stopwords, calculate and return the frequency of the words(will be shown below) in India and US respectively, in a data frame. These words are “electricity”, “free wifi”, “clean water”, “toilet”, “prosperity”, “election”, “voting”, “campaign”. Show these words their ranking, word_count and probability in a dataframe and produce several csv files. 


3.	Rank all the words in the text according to their frequency (from high to low) in a table. Show the rankings of these words “electricity”, “free wifi”, “clean water”, “toilet”, “prosperity”, “election”, “voting”, “campaign”. There must be many other words that may appear more frequently than all those words, for example, “banana”. I have shown the expected table in Note below. Finally, use logistic regression. (India: 1; US: 0)


Result

Code
1.	Twitter_API.py will get small filtered data (with “#Democracy” and location either from the “US” or “India”)
2.	merge_data.py can merge the small filtered data with the big filtered_data.csv that I have accumulated (Now I have about 1800 filtered tweets from the US and more than 600 from India. Ideally, I should get 10000 or more).
3.	process_data.py will analyse the filtered_data.csv and produce two regression graphs and six csv files.

Analysis
1.Because the lack of data, I can only prove half of my theory. In the US, the word bunch “election”, “voting”, “campaign” have higher probability than in India.

US
word	ranking	word_count	probability
voting	    136	    23	    0.00093276
election	8	    98	    0.003974369
campaign	1919	3	    0.000121664
electricity	5262	0	    0
wifi	    5262	0	    0
clean water	5262	0	    0
toilet	    5262	0	    0
prosperity	620	    8	    0.000324438


India
word	ranking	word_count	probability
voting	    189	    8	    0.00086815
election    286	    6	    0.000651112
campaign	1629	0	    0
electricity	1629	0	    0
wifi	    1629	0	    0
clean water	1629	0	    0
toilet	    1629	0	    0
prosperity	1629	0	    0



2.Because of the lack of data, the regression graphs cannot say too much, but they will show after running process_data.py

3.By analyzing india_ranking.csv and usa_ranking.csv, I found the word “eat” can also be used in this project. In the US, “eat” ranks the 1049th and in India, “eat” ranks the 263rd. So, I may say, Indian tweeter users are more likely to associate democracy with food or eating more often than tweeter users in the US. If I have enough data, I may find more similar words that would have more explanatory power.

4. In the future, I can use this code to do more extended work. For example, I can scrape data from more countries other than US and India and I can compare word association with more concepts of social institutions, such as “#constitution”, etc.

5. "Prosperity" is not a good choice in this project, probably because People in India seldom use this high-sounding word in tweeting.
