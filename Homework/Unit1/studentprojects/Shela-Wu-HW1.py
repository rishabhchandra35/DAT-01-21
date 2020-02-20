### FUNCTION 1

def find_user(screen_name, *keys):
    import requests
    from requests_oauthlib import OAuth1
    
    # passing through tokens
    url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name='
    auth = OAuth1('BgbMwM2JNDTYW0i7520Id2zbr', 'iktnfFhMFyJYOvVleNlcTZrv6RGG7rNlnQ0zjqzG6norR3Rcul', '1222956016268140556-FMCHVy0GZVvhput4OxVSw89QhFbcSr', 'aBPxLEfVR5xoWug5vPEc4jJldAP6i72U4WFoidagXSmg8')
    data = requests.get(url+screen_name, auth=auth).json()
    
    # if specified, apply this loop
    if keys:
        key_dict = {}
        for key in keys:   # returns list
            for k in key:  # parse through each element in list
                key_dict[k] = data[0][k]
        return key_dict
            
        
    return data




### FUNCTION 2
# Function takes in a hashtag to run on search through tweet DB
# can return a certain limit of tweets and limit result 
# do so through appending appropriate text to query string

def find_hashtag(hashtag, **specifications):
    import requests
    from requests_oauthlib import OAuth1
     # passing through tokens
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23'
    auth = OAuth1('BgbMwM2JNDTYW0i7520Id2zbr', 'iktnfFhMFyJYOvVleNlcTZrv6RGG7rNlnQ0zjqzG6norR3Rcul', '1222956016268140556-FMCHVy0GZVvhput4OxVSw89QhFbcSr', 'aBPxLEfVR5xoWug5vPEc4jJldAP6i72U4WFoidagXSmg8')
    
    # Create gatekeeper to check for hashtag in argument 
    if '#' in hashtag:       # if '#' exists, exclude from hashtag string
        hashtag = hashtag[1:]
    
    complete_url = url + hashtag
    
    if "count" in specifications:
        complete_url = complete_url + '&count=' + str(specifications['count'])
    
    if "search_type" in specifications:
        complete_url = complete_url + '&result_type=' + specifications['search_type']
    
    data = requests.get(complete_url, auth=auth).json()
    
    return data['statuses'] 




### FUNCTION 3
# GET all the followers information that's released as dictionary under 'users' key-value 
# provide option for specified keys
# have ability to toggle dataframe

def get_followers(screen_name, keys = ['name', 'followers_count', 'friends_count','screen_name'], to_df = False):
    import requests
    from requests_oauthlib import OAuth1
    import pandas as pd
    
     # passing through tokens
    url = 'https://api.twitter.com/1.1/followers/list.json?screen_name='
    auth = OAuth1('BgbMwM2JNDTYW0i7520Id2zbr', 'iktnfFhMFyJYOvVleNlcTZrv6RGG7rNlnQ0zjqzG6norR3Rcul', '1222956016268140556-FMCHVy0GZVvhput4OxVSw89QhFbcSr', 'aBPxLEfVR5xoWug5vPEc4jJldAP6i72U4WFoidagXSmg8')
    data = requests.get(url+screen_name,auth=auth).json()
    
    # Create centralized list 
    #info_list = []
    #for key in keys:
    #    info_list.append(data['users'])
    
    final_list = []
    
    for user in data['users']:    # user = each user's info as dictionary
        user_dict = {}            # creates dictionary for each user     
        for key in keys:          # creates key and attachs value
            user_dict[key] = user[key]
        final_list.append(user_dict)
            
    
    if to_df:
        df_dict = {}        # created a new dict for dataframe where we create a list for each key
        for key in keys:    # looping through each key, creating dict entry per key with value as list
            df_dict[key] = [user[key] for user in final_list]  # loops through each user dictionary
        df = pd.DataFrame(df_dict)
        return df
    
    
    ### LEFT MY OLD CODE FOR MY OWN REFERENCE :) please ignore!
    
    #final_list = []
    #for inner_list in info_list:
    #    for user in inner_list:
    #        final_list.append(user)
    #    break     # otherwise first for loop will repeat 4 more times and create duplicates
   

    # Create list of all values for name key, etc.
    #names_list = [names['name'] for names in final_list]
    #follower_ct_list = [names['followers_count'] for names in final_list]
    #friends_ct_list = [names['friends_count'] for names in final_list]
    #screen_name_list = [names['screen_name'] for names in final_list]
    
    
    # Create dictionary to turn into df
    #data_dict = {
    #    'Name': names_list,
    #    'Follower Count': follower_ct_list,
    #    'Friend Count': friends_ct_list,
    #    'Screenname': screen_name_list
    #}
    
    
    # To show data frame or not
    #if to_df:
    #    df = pd.DataFrame(data_dict)    
    #    return df
    #else:
    #    unformatted_list = []
    #    for i in range(len(names_list)):
    #        user_dict = {}
    #        user_dict['Name'] = data_dict['Name'][i]
    #        user_dict['Follower Count'] = data_dict['Follower Count'][i]
    #        user_dict['Friend Count'] = data_dict['Friend Count'][i]
    #        user_dict['Screenname'] = data_dict['Screenname'][i]
    #        unformatted_list.append(user_dict)
    #    return unformatted_list
            