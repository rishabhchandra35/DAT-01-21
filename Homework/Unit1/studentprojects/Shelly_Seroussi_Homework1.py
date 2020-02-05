import requests
from requests_oauthlib import OAuth1
from urllib.parse import urlencode
import pandas as pd

auth = OAuth1('nApIvjlwjgExypH0LPzYSHm2v', 'nSychb5oEHcWftdayZibvuoGnmaqPHhDS0Rhnmh4f3b6QZECC2',
               '421909403-cmBNHYTEay8RSVS4aPtPvUrvOEpoaIHykWW7UbzB', 'GQM5BdM73br8Xgt6Ml5lbw5X5XHsZLVCDe0VkZB8Pb0We')

def find_user(screen_name, keys=[]): 
    if screen_name.find('@') == 0:
        clean_name = screen_name.replace('@', '', 1)
    url = f"https://api.twitter.com/1.1/users/show.json?screen_name={clean_name}"
    userObject = requests.get(url, auth=auth).json()
    newUserObject = {}
    if keys:
        for key in keys:
            if key in userObject:
                newUserObject[key] = userObject[key]
        return newUserObject
    return userObject
    
def find_hashtag(hashtag, count=15, search_type='mixed'):
    clean_hashtag = hashtag
    if search_type != 'mixed' or search_type != 'popular' or search_type != 'recent':
        search_type = 'mixed'
    if hashtag.find('#') != 0:
        clean_hashtag = f'#{hashtag}'
    params = urlencode({'q': clean_hashtag, 'count': count, 'search_type': search_type})
    url = f"https://api.twitter.com/1.1/search/tweets.json?{params}"
    tweetObject = requests.get(url, auth=auth).json()
    return tweetObject


def get_followers(screen_name, keys=['name','followers_count', 'friends_count', 'screen_name'], to_df=False):
    clean_name = screen_name
    newFollowersList = []
    followersData = {}
    if screen_name.find('@') == 0:
        clean_name = screen_name.replace('@', '', 1)
    params = urlencode({'q': clean_name})
    url = f"https://api.twitter.com/1.1/followers/list.json?{params}"
    followers = requests.get(url, auth=auth).json()
    for follower in followers['users']:
        followerObject = {}
        for key in keys:
            followerObject[key] = follower[key]
        newFollowersList.append(followerObject)
    if to_df:
        for key in keys:
            print(key)
            followersData[key] =  [follower[key] for follower in followers['users']]
        df = pd.DataFrame(followersData)
        df.head()
        return df
    return newFollowersList

    