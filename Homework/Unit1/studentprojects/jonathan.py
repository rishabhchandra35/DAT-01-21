# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:10:43 2020

@author: Jonat
"""

import requests
from requests_oauthlib import OAuth1

# passing in my developer tokens to the OAuth1 function
tokens = OAuth1('NOZHm1aLT1AVmchGbCmiZOAga', 'nPyaYCt8L7ymqGZtU8EqC0a2ypI9aSJgVNIhtoZ0wGsaf3BJw9',
                '1079981876864008192-AlhO4yOa06oW2sXZpLpWPwnOxEERYS', 'o3E0AsKJfDoTBk77UQYExzOG7E46jPYvpWNGAKsD6lUBY')

# since we're going to re-use this several times, we'll wrap it up into our own function
def check_handle(twitter_handle):
    # check if twitter handle begins with @
    if twitter_handle[0] == '@':
        # and if so slice it out
        return twitter_handle[1:]
    # otherwise just return the handle as is
    return twitter_handle

def find_user(screen_name, keys=None):
    
    # verify the screen_name
    screen_name=check_handle(screen_name)
    
    # base url we're going to work with
    base_url = 'https://api.twitter.com/1.1/users/lookup.json'
    # query we're going to attach
    query_string   = f'?screen_name={screen_name}'
    
    # the results return a list -- so we're just going to get the first (and only) item out of it
    results  = requests.get(base_url+query_string, auth=tokens).json()[0]
    
    # if something was provided for keys 
    if keys is not None:
        # then make a new dictionary out of the set of keys provided
        new_results = {key: results[key] for key in keys}
        # and return this
        return new_results
    
    # and if the if statement above wasn't true, then just give back the whole thing
    return results