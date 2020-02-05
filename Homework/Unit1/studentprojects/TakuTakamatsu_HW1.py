#!/usr/bin/env python
# coding: utf-8


#import all necessary modules
import requests
from requests_oauthlib import OAuth1


# In[ ]:


#store the API tokens and keys in variables
api_key = 'SWrPWw32a0wLMOQ8ezBQhWzIv'
api_secret_key = 'tSoT7EXGaO9TzFVhwN3AJToA2K7ojPSQxbTojW0E1JfOcn41HY'
access_token = '477582190-EBHb6a9d7xObLWK6uyM66FgkhZFvAh99PlZVyLoj'
access_token_secret = 'jrgUJvMOwiQCVYjyxrPJV7nT0NGnzYIPNFywVEh92duhC'


# In[ ]:


#store the OAuth1 function in a varible for easy access
auth = OAuth1(api_key, api_secret_key, access_token, access_token_secret)


# In[ ]:


#FUNCRION 1: Finding user entered with screen_name argument
#define function with arguments: screen_name and keys(optional)
def find_user(screen_name, keys=[None]):
    #remove '@' symbol if present in screen_name
    if screen_name[0] == '@':
        screen_name = screen_name[1:]
    
    #append screen_name to url and request
    url = 'https://api.twitter.com/1.1/users/show.json?screen_name='
    user_object = requests.get(url+screen_name, auth=auth).json()
    
    #if no keys are entered, return entire user object
    if keys == None:
        return user_object
    #else, search for the specific keys in the user_object, and return them in a new dictionary
    else:
        user_desc = {}
        for key in keys:
            user_desc[key] = user_object[key]
        return user_desc


# In[ ]:


#FUNCTION 2: Finding tweets with hashtag entered
#define function with arguments: hashtag, count, search_type (optional)
def find_hashtag(hashtag, count=None, search_type=None):
    
    #insert/replace'#' character with %23
    h = '%23'
    if hashtag[0] == '#':
        hashtag = h + hashtag[1:]
    else:
        hashtag = h + hashtag
    
    #place root url and search types into variables
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='
    search_types = ['mixed','recent','popular']
    
    
    #search using the arguments given
    try:
        if count == None and search_type == None:
            search = requests.get(url+hashtag, auth=auth).json()
        elif search_type in search_types:
            search = requests.get(url+hashtag+'&result_type='+search_type, auth=auth).json()  
        elif count <= 100 and count > 0:
            search = requests.get(url+hashtag+'&count='+str(count), auth=auth).json()
        elif count <= 100 and count > 0 and search_type in search_types:
            search = requests.get(url+hashtag+'&count='+str(count)+'&result_type='+search_type, auth=auth).json()
        return search
    
    #try statement to avoid inaccurate parameters. ie. count > 100 or count < 0
    except:
        print("Invalid parameters")


# In[ ]:


#FUNCTION 3: finding followers with screen_name entered and parameters
#define function with arguments: screen_name, keys and to_df boolean (default False)
def get_followers(screen_name, keys=['name', 'followers_count', 'friends_count', 'screen_name'], to_df=False):
    #remove '@' symbol if present in screen_name
    if screen_name[0] == '@':
        screen_name = screen_name[1:]
    
    #search twitter data objects of every follower
    url = 'https://api.twitter.com/1.1/followers/list.json?screen_name='
    data = requests.get(url+screen_name, auth=auth).json()
    
    #loop through each follower's keys and append to an empty dictionary
    #append the dictionary to a new list
    user_dict = []
    for user in data['users']:
        user_keys = {}
        for key in keys:
            user_keys[key] = user[key]
        user_dict.append(user_keys)
    
    #if to_df is set to True, import pandas and return data frame
    if to_df == True:
        import pandas as pd
        return pd.DataFrame(user_dict)
    else:
        return user_dict


# In[ ]:


#FUNCTION 4: finding list of common followers through two screen_names
#define function with arguments: names (list), keys (optional), and to_df boolean (default False)
def friends_of_friends(names, keys=[None], to_df=False):
    #place the names list into two separate variables
    user_1, user_2 = names[0], names[1]
    #remove '@' symbol if present in name
    if user_1[0] == '@':
        user_1 = user_1[1:]
    if user_2[0] == '@':
        user_2 = user_2[1:]

    #root url to authenticate:
    url = 'https://api.twitter.com/1.1/followers/list.json?screen_name='

    #search API for the first user's followers and append to a new list
    user_1_object = []
    data_1 = requests.get(url+user_1, auth=auth).json()
    for user in data_1['users']:
        if keys == [None]:
            user_1_object.append(user)
        else:
            user_1_dict = {}
            for key in keys:
                user_1_dict[key] = user[key]
            user_1_object.append(user_1_dict)
    
    #search API for the second user's followers and append to a new list
    user_2_object = []
    data_2 = requests.get(url+user_2, auth=auth).json()
    for user in data_2['users']:
        if keys == [None]:
            user_2_object.append(user)
        else:
            user_2_dict = {}
            for key in keys:
                user_2_dict[key] = user[key]
            user_2_object.append(user_2_dict)

    #compare both user objects and append to new list if id's match
    common_followers = []
    for user in user_1_object:
        for user_2 in user_2_object:
            if user['id'] == user_2['id']:
                common_followers.append(user)

    #if to_df is set to True, import pandas and return as data frame
    if to_df == True:
        import pandas as pd
        return pd.DataFrame(common_followers)
    else:
        return common_followers


# In[ ]:


#FUNCTION 5: finding entire list of common followers, cursoring through entire user object
#friends_of_friends argument with additional full_search argument (boolean, default False)
def friends_of_friends(names, full_search=False, keys=[None], to_df=False):
    
    #import time function to avoid API limit error
    import time
    
    #place the names list into two separate variables
    user_1, user_2 = names[0], names[1]
    #remove '@' symbol if present in name
    if user_1[0] == '@':
        user_1 = user_1[1:]
    if user_2[0] == '@':
        user_2 = user_2[1:]

    #root url to authenticate:
    url = 'https://api.twitter.com/1.1/followers/list.json?screen_name='

    #if full_search is set to True, iterate through each page of the search using a counter variable (next_cursor)
    if full_search == True:
        #enter while loop to search through each page of user 1
        user_1_object = []
        next_cursor = -1
        while True:
            try:
                data_1 = requests.get(url+user_1+'&cursor='+str(next_cursor), auth=auth).json()
                for user in data_1['users']:
                    if keys == [None]:
                        user_1_object.append(user)
                    else:
                        user_1_dict = {}
                        for key in keys:
                            user_1_dict[key] = user[key]
                        user_1_object.append(user_1_dict)
                #if next_cursor is 0, it means there are no remaining pages, thus break loop
                next_cursor = data_1['next_cursor']
                if next_cursor == 0:
                    break
            except:
                #if API limit is reached, an error is raised. Avoid that happening with an exception,
                #and sleep for 15 minutes. 
                print("API limit reached -- sleeping for 15 minutes")
                time.sleep(15*60)
    
        #enter while loop to search through each page of user 2
        user_2_object = []
        next_cursor = -1
        while True:
            try:
                data_2 = requests.get(url+user_2+'&cursor='+str(next_cursor), auth=auth).json()
                for user in data_2['users']:
                    if keys == [None]:
                        user_2_object.append(user)
                    else:
                        user_2_dict = {}
                        for key in keys:
                            user_2_dict[key] = user[key]
                        user_2_object.append(user_2_dict)
                next_cursor = data_2['next_cursor']
                if next_cursor == 0:
                    break
            except:
                print("API limit reached -- sleeping for 15 minutes")
                time.sleep(15*60)

    #if full_search set to False, perform search for one page only - same as Function 4
    else:
        user_1_object = []
        data_1 = requests.get(url+user_1, auth=auth).json()
        for user in data_1['users']:
            if keys == [None]:
                user_1_object.append(user)
            else:
                user_1_dict = {}
                for key in keys:
                    user_1_dict[key] = user[key]
                user_1_object.append(user_1_dict)
        user_2_object = []
        data_2 = requests.get(url+user_2, auth=auth).json()
        for user in data_2['users']:
            if keys == [None]:
                user_2_object.append(user)
            else:
                user_2_dict = {}
                for key in keys:
                    user_2_dict[key] = user[key]
                user_2_object.append(user_2_dict)

    #compare both user objects and append to new list if id's match
    common_followers = []
    for user in user_1_object:
        for user_2 in user_2_object:
            if user['id'] == user_2['id']:
                common_followers.append(user)

    #if to_df is set to True, import pandas and return as data frame
    if to_df == True:
        import pandas as pd
        return pd.DataFrame(common_followers)
    else:
        return common_followers

