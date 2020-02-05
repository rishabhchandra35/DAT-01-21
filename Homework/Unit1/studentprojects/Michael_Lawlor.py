#Michael Lawlor
#Homework, Unit 1
#Data Science DAT-02-21
#Feb 4th, 2020

#README - To run this file it is assumed the user will execute "from HW1_Michael_Lawlor import* "

import requests
from requests_oauthlib import OAuth1    #import OAuth function
# ML's Twitter developer account tokens:
Tokens = OAuth1('GdcMKOsy3PL0ZpHq6OFPbLvpB', 'j0OeyMAd3B1W7kf406q4bER5iPQ5oHzdGBEPSZOOHjxMgwCyM6','1198289133279621120-hnHzjpobl825HvFLwz1mDR2nqJ3Ikl', 'OVS1NWejHsbsP8X5QAMJ05ujBmiNXCz1GPPpMyld7SzPL')


def find_user(screen_name, keys=[]):   #returns an object with Twitter user information
    # If keys are provided, only the key characteristics are returned for each item.
    screen_name=screen_name.replace('@','')     #removes the @ character from the scren_name
    url='https://api.twitter.com/1.1/users/lookup.json?screen_name='+screen_name        #concatenate search URL with screen name
    results=requests.get(url, auth=Tokens).json()[0]        #[0] returns the search results and ignores the search summary which is located in [1]
    if keys==[]:           #return results as-is if no keys provided
        return results
    results=[results[item] for item in keys if item in results]  #Creates new results list with items containing only the key-value pairs specified
    return results


def find_hashtag(hashtag, count, search_type):   #searches for the provided hashtag
    #Count (optional) integer, specifies number of search results
    #Search (optional) type must be = mixed, recent, or popular
    hashtag=hashtag.replace('#','')         #removes # character if present.  It is added in the search URL
    hashtag=hashtag.replace(' ','%20')     #converts sppace to UTF-8 format
    url='https://api.twitter.com/1.1/search/tweets.json?q=%23'+hashtag  #concatenates hashtag to search URL
    if search_type!=None:   #if a search type is provided, it is concatenated to the search URL
        url=url+'&result_type='+search_type
    if count!=None:         #if a count is specified, it is concatenated to the search url
        url=url+'&count='+str(count)
    results=requests.get(url, auth=Tokens).json()['statuses'] #returns the status objects
    return results


def get_followers(screen_name, keys=[], to_df=False):   #returns a list or dataframe of followers for the screen_name provided
    #If keys are provided it returns the only key-value pairs specified for the results objects
    #Keys provided that do not exist in the results are ignored
    screen_name = screen_name.replace('@', '')      #removes @ character from screen_name
    url = 'https://api.twitter.com/1.1/followers/list.json?screen_name=' + screen_name      #concatenates screen name to search URL
    results = requests.get(url, auth=Tokens).json()['users']        #returns only the user values of the results

    if keys != []:  # if keys are provided, the results are
        out = []    #reset output to empty list
        for item in results:
            out.append([item[key] for key in keys if key in item])  #iterate through results and append items to the output if the matching key is specified
        results = out
    if to_df == True:
        import pandas as pd
        results = pd.DataFrame(results)  #convert results to a PANDAS data frame if to_df is True
    return results



def friends_of_friends(names, keys=[], to_df=False):        #returns 3 common followers for two users provided in a list
    # If keys are provided it returns the only key-value pairs specified for the results objects
    # Keys provided that do not exist in the results are ignored
    names = [name.replace('@', '') for name in names]  #removes @ character from screen_name
    #initialize variables
    results0 = []
    results1 = []
    cursor0 = '-1'
    cursor1 = '-1'
    out = []
    iter=0
    while len(out) < 3 and iter<5:     #iterate with cursored search results to ensure at least 3 users found. max 5 loops to avoid time outs/infinte loops
        url = 'https://api.twitter.com/1.1/followers/list.json?screen_name=' + names[0] + '&count=200&cursor=' + cursor0
        results0.append(requests.get(url, auth=Tokens).json())
        cursor0 = [results0[0]['next_cursor_str']]      #Extract next cursor string from results
        url = 'https://api.twitter.com/1.1/followers/list.json?screen_name=' + names[1] + '&count=200&cursor=' + cursor1
        results1.append(requests.get(url, auth=Tokens).json())
        cursor1 = [results1[0]['next_cursor_str']]      #Extract next cursor string from results

        results0 = results0[0]['users']      #Extract users from results
        results1 = results1[0]['users']      #Extract users from results
        out = []
        #iterate through both user's results lists to check for matches.  append matches to the list 'out'
        for item in results0:
            for obj in results1:
                if item['id'] == obj['id']:
                    out.append(item)
        iter=iter+1

    #iterate through the matches and build a new output with only the key-value pairs for specified keys
    results = []
    for item in out:
        results.append([item[key] for key in keys if key in item])

    #convert to Data Frame if to_df=True
    if to_df == True:
        import pandas as pd
        results = pd.DataFrame(results)

    return results[:3]  #Return only the first three items.  This can be modified if more items are desired.