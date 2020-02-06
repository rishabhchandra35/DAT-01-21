"""
.py file containing functions for interacting with Twitter's api.
in test_twitterfuncs.py, you will find functions that test the functionality and return the responses
of each function using a few different scenarios
"""
import requests
from requests_oauthlib import OAuth1
import pandas as pd

tokens = OAuth1('sWjlYbgUANObCyZ1YPeKerP3K', 'j7tbbJmTGKFqSG1RXjNfVU3dY9j54oQ0UU0tAwDqmtuE4Fv8BD'
              ,'1223025397035606017-VuF2llYRiSepf0XS8O8i4nikToLCr9', 'BIX3EPvTLGoyBrDnp9cXSeQeq6xeoz6gl73xcCAfWidg9')
searchtwt = 'https://api.twitter.com/1.1/search/tweets.json'
flwerlist = 'https://api.twitter.com/1.1/followers/list.json?'
user_search = 'https://api.twitter.com/1.1/users/show.json?'
tweet_search = 'https://api.twitter.com/1.1/search/tweets.json'
q = '?q='
chars = {'space': (' ', '%20'), 
        'hashtag': ('#', '%23')}

def find_user(screen_name, keys=None):
    """
    parameters
    ------------
    screen_name: str
        Twitter handle to search for. Can have @ or not.
    keys: list; optional
        keys to return about user object
    
    return
    ------------
    dict of user object
    """
    # remove @ if passed to arg with it
    screen_name = screen_name.replace('@', '')
    search = 'screen_name=' + screen_name
    # request the user search
    r = requests.get(user_search + search, auth=tokens)
    # call request to get the user dictionary
    user_dict = r.json()
    dkeys = user_dict.keys()
    # check to see if there is an issue getting screen name
    if 'errors' in dkeys:
        print(user_dict['errors'])
        return False
    # check to see if keys entered are not a part of returned dict
    if keys:
        # get list of keys not in dict
        missing_keys = [key for key in keys if not key in dkeys]
        if missing_keys:
            print('The following keys are not in the user object :')
            for key in missing_keys:
                print(key)
            print('\nPlease try again')
            return False
        # return dict with only keys the user wants
        info = {key: user_dict.get(key,'Not in dict') for key in keys}
        return info
    
    # return dict with all keys of user_dict
    return user_dict


def find_hashtag(hashtag, count=None, search_type='mixed'):
    """
    parameters
    ------------
    hashtag: str
        text to use as a hashtag search
    count: int, optional
        number of results to return
    search_type: str, optional
        type of results to return. accepts only 3 options:
            - mixed: return mix of most recent and most popular results
            - recent: return most recent results
            - popular: return most popular results
    
    return
    ------------
    list of data object that contain information about each tweet that matches the hashtag provided as input
    """
    # make sure the user input a valid search type
    assert (search_type not in ('mixed', 'recent', 'popular')), 'search_type not in options. Select one of the following:\n("mixed", "recent", "popular")' 
    # add hashtag if user did not input it
    hashtag = hashtag if '#' != hashtag[0] else '#' + hashtag
    # convert # into version twitter api needs
    hashtag = hashtag.replace(*chars['hashtag'])
    url = tweet_search + q + hashtag

    # make different requests given option count parameter
    if not count:
        r = requests.get(url + '&search_stype=%s' % search_type, auth=tokens)
    else:
        r = requests.get(url + '&count=%s&search_stype=%s' % (count, search_type), auth=tokens)
    # get dict of tweets
    data = r.json()
    # return list of tweets (as dicts)
    return data['statuses']


def get_followers(screen_name, keys=['name', 'followers_count', 'friends_count', 'screen_name'], to_df=False):
    """
    parameters
    ------------
    screen_name: str
        twitter handle to search for
    keys: list; defaults to ['name', 'followers_count', 'friends_count', 'screen_name']
        keys to return for each user
    to_df: bool; defaults to False
        if True, returns a DataFrame object of the data objects


    return
    ------------
    list or DataFrame of data objects for each of the users followers;
    returning values specified by the keysS
    
    """
    # remove @ if passed to arg with it
    screen_name = screen_name.replace('@', '')
    search = 'screen_name=' + screen_name
    # get requestg for followers list of user
    r = requests.get(flwerlist + search, auth=tokens)
    # get dict of user dicts 
    user_dict = r.json()
    # check to see if screen name exists
    if 'errors' in user_dict.keys():
        print(user_dict['errors'])
        return False

    # extract list of users from dict
    users = user_dict['users']
    # check for missing keys
    missing_keys = [key for key in keys if not key in users[0].keys()]
    if missing_keys:
        print('The following keys are not in the user object :')
        for key in missing_keys:
            print(key)
        print('\nPlease try again')
        return False
    
    # create a list of user dicts with only keys that were passed
    user_list = [{key: user[key] for key in keys} for user in users]
    # create DataFrame object to return if to_df is True
    if to_df:
        df = pd.DataFrame(user_list)
        return df
    
    # return user_list as a list of dicts
    return user_list


def friends_of_friends(names, keys=None, to_df=False, full_search=False):
    """
    parameters
    ------------
    names: list of length two
        list of two Twitter users to compare friends list with
    keys: list; default set to None
        list of keys to return for information about each user
    to_df: bool; default set to False
        returns a DataFrame object if set to True
    full_search: bool; default set to False
        if set to True, will cursor through all followers of the 
        users until there are no more, or api limit has been 
        exceeded

    return
    ------------
    list or DataFrame of data objects for each user that two Twitter
    users have in common
    """
    # assert that list contains only two users
    assert(not len(names) > 2) , 'Please enter only two users'
    # remove @ symbol if included
    names = [name.replace('@', '') for name in names]
    # get dict of user dicts for each name passed to function
    name_flws = {}

    # check to see if user wants a full search
    # the full search takes a cursor and requests the api through all of the cursors until
    # the data is empty or api rate limit is exceeded
    if full_search:
        # loop through each name requested by user
        for name in names:
            # initialize cursor
            cursor = -1
            # catch a KeyError becasue either the rate limit exceeded or the screen_name is
            try:
                # keep getting a request for more followers until cursor is 0
                while cursor:
                    # set search query to include cursor
                    search = 'screen_name=' + name + '&cursor=%s' % cursor
                    r = requests.get(flwerlist + search, auth=tokens)
                    # get request to return a dict that contains the list of user dicts in 'users'
                    user_dict = r.json()
                    # set the cursor to next cursor from last request
                    cursor = user_dict['next_cursor']
                    # check if name is already in dict, if not create list of user dicts
                    if not name in name_flws.keys():
                        name_flws[name] = [user_dict]
                    else:
                        name_flws[name].append(user_dict)
            except KeyError as e:
                print("Key Error", e)
                print(user_dict['errors'])
    else:    
        for name in names:
            search = 'screen_name=' + name
            r = requests.get(flwerlist + search, auth=tokens)
            name_flws[name] = [r.json()]       
    
    # Due to a issues with the api rate limit, the function will end here
    # if follower information wasn't returned for each name requested
    assert (len(name_flws.keys()) == 2), 'Both names were not returned'
    
    # check to see if screen names exist
    errors = []
    for name in name_flws.keys():
        if 'errors' in name_flws[name][0].keys():
            errors.append('%s Error. %s.' % (name, name_flws[name][0]['errors']))
    if errors:
        for msg in errors:
            print(msg)
        return False

    # check for missing keys
    if keys:
        missing_keys = [key for key in keys if not key in name_flws[name][0]['users'][0].keys()]
        if missing_keys:
            print('The following keys are not in the user object :')
            for key in missing_keys:
                print(key)
            print('\nPlease try again')
            return False
     
    # create users_dict to get just the user dicts of each follower
    users_dict = {}
    for name, list_of_dicts in name_flws.items():
        # name and list of dicts containing list of user dicts
        # create dict of name: list of user dicts
        for d in list_of_dicts:
            # extract all the users from each dict
            for i in d['users']:
                if not name in users_dict.keys():
                    users_dict[name] = [i]
                else:
                    users_dict[name].append(i)

    # create the friends of friends list by checking if the user ids match
    fof_list = [user1 for user1 in users_dict[names[0]] for user2 in users_dict[names[1]] if user1['id'] == user2['id']]
    if not fof_list:
        print("No users in common")
        return fof_list
    
    # create a list of user dicts with only keys that were passed
    if keys:
        fof_list = [{key: user[key] for key in keys} for user in fof_list]

    if to_df:
        df = pd.DataFrame(fof_list)
        return df
    
    return fof_list


