#!/usr/bin/env python
# coding: utf-8

# ## Homework 1: Advanced Track -- Harvest the Twitter API

# **Objective:** Write a series of functions that allow you to dynamically harvest Twitter data.
# 
# **Estimated Time to Complete:** 4-12 hours
# 
# #### Sections
# 
#  - **Section 1:** Setting up your developer account, using OAuth1 authentication (approx 45-120 minutes)
#  - **Sections 2 & 3:** Navigating the API documentation, getting your first query strings (approx 45-120 minutes)
#  - **Section 3:** Writing your API calls (approx 90 - 360 minutes)
#  
# #### What You'll Turn In:  
#  - A `.py` (not a Notebook!) file that contains the functions that you were prompted to create.  These should contain comments demonstrating why your code does what it does, and after it's run, the instructor should be able to make the appropriate function calls in Spyder or any other IDE.

# ## Section 1:  Setting Up Your Developer Account

# Most API's require you to do a little pre-work in order to be able to use them, so the first part of this homework assignment will be spent setting up your developer account so you have API Access.

# **Step 1:  Create a Twitter Developer Account**
# 
#  - Make sure you have a regular twitter account before you do this
#  - You can apply for a developer account here:  https://developer.twitter.com/en/apply-for-access
#   - Choose either a student or hobbyist/personal account

# **Step 2:  Create An App**
# 
# You don't have to intend to build an official software program to have an app.....this is just a way for you to get authentication keys to use with the API.
# 
#  - Go to the menu in the upper right hand corner and click on **Your Name** > **Apps**
#  - Choose **Create An App**
#  - You'll be prompted to enter some information about your app.  Don't worry too much about this, it can say almost anything.  You'll be prompted to list websites where it will be hosted...this can be anything for now.  Use https://generalassemb.ly if you're undecided about what to put.

# **Step 3: Create Your API Tokens**
# 
# Now that you have an app, you can use its API tokens to go ahead and make requests like we did in class 3.  Like a lot of API's, the Twitter API uses something called OAuth authentication.  
# 
# If you didn't wait until the night before this assignment was due and have a spare 30 minutes, you can read a little about it here: https://oauth.net/
# 
# In any event, you need API tokens in order to make requests.  Do the following:
# 
#  - Go to the **Apps** section of your developer portal
#  - Click on the **Details** button for the app that you just created
#  - Click on the **Keys & Tokens** tab
#  - Generate your Access Token and Access Token Secret keys.  You'll need to write these down when you're done
# 
# Now you're ready to make requests to the Twitter api.  Everytime you make a request, you'll need to include the 4 tokens you just created.  (You can always regenerate them for whatever reason).  

# **Step 4:  Your First Request**
# 
# To make requests to the Twitter API you're going to need a module which is **not** already pre-installed in Anaconda. You'll need to install it via PIP, which is python's package manager.  It's called `requests_oauthlib`.  You can install this via Anaconda Prompt or Terminal by simply typing in the command `pip install requests_oauthlib`, and then you'll be finished.
# 
# The logistics of making an OAuth1 authenticated request are very similar to what was done in class 3, but with a few additional steps.  You can see how to do it here:  https://requests.readthedocs.io/en/master/user/authentication/#oauth-1-authentication.  The only thing you'll need to change is the info for your API tokens that are passed into the `OAuth1()` function.
# 
# Try making a request to the following URL to confirm that it works: 'https://api.twitter.com/1.1/account/verify_credentials.json'

# In[24]:


import requests
from requests_oauthlib import OAuth1

tokens = OAuth1('NOZHm1aLT1AVmchGbCmiZOAga', 'nPyaYCt8L7ymqGZtU8EqC0a2ypI9aSJgVNIhtoZ0wGsaf3BJw9',
                '1079981876864008192-AlhO4yOa06oW2sXZpLpWPwnOxEERYS', 'o3E0AsKJfDoTBk77UQYExzOG7E46jPYvpWNGAKsD6lUBY')

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

req = requests.get(url, auth=tokens).json()


# In[25]:


req


# If you get your json object back, then you're good to go.

# ## Section 2: Searching Tweets

# Most websites you access will have a long string attached to the end of them that look something like this:  `http://thewebsite.com/?year=2019&color=golden%20yellow%20user_id=48549395959438`.
# 
# Most people have no reason to pay attention to any of this, but all the special symbols at the end are basically encoded commands that say 'return a website that displays x,y,z characteristics.'  
# 
# When accessing api data, it basically works the same way.

# **Step 1:  Set Up Your First Query String**

# If you go into Twitter and search for the term `Data Science`, you should be brought to a url that looks like this:  `https://twitter.com/search?q=Data%20Science&src=typed_query`
# 
# If you'd like, you can drop the `&src=typed_query` from the url and still get the same results.
# 
# There are some important details to pay attention to:
# 
#  - Like class 3 when we worked with GitHub, there is a **base url**.  In this case it's `https://twitter.com/search`
#  - Whenever you enter a search for something, the base url will be followed by something that looks like `?q=My%20Search%20Term`
#   - The `?` marks the beginning of the query string.  This basically says 'initiate a request with whatever parameters that follow'
#   - The `q` is a **parameter**, essentially some condition to pass into the query string that determines what results will be given back to you.
#   
# **Useful Thing To Do Right Now:** Go back to the Twitter search page, and just try searching for different things, and notice what shows up after the `q=`.  Here are some questions to ask yourself:
# 
#  - How are white spaces encoded?  Ie, if you search for `Jonathan Bechtel` in the search box, what shows up to account for the space between the two words?
#  - What about hash symbols?  If you search for `#MeToo`, `#GirlsWhoCode` or `#DataScience`, what happens with that `#` symbol?
#  - Once you get the hang of this, see if you can just re-create some searches yourself by creating the url directly, and bypassing the search box altogether.
# 
# Now, let's try and make a request for a search for `Data Science`.  
# 
# If you look at Twitter's docs, you'll see that the base url for the search API is `'https://api.twitter.com/1.1/search/tweets.json`
# 
# This means you have to add the `?q=Whatever%20Word%20%Goes%20Here` to the end to complete the search.
# 
# So go ahead, and see if you can create your API call for a search for the term `Data Science`.
# 
# If you did it correctly, you should have a dictionary with a key called `statuses`, and it'll be a list with all of the tweets returned by your search.  

# In[26]:


# your answer here
base_url = 'https://api.twitter.com/1.1/search/tweets.json'
search = '?q=data%20science&src=typed_query'

req = requests.get(base_url + search, auth=auth).json()


# In[27]:


req


# For good measure, try doing a search for tweets relating to `#MeToo` as well.

# In[4]:


# your answer here
base_url2 = 'https://api.twitter.com/1.1/search/tweets.json'
search2 = '?q=%23MeToo&src=typed_query'

req2 = requests.get(base_url + search, auth=auth).json()
req2


# **Step 2:  Adding Parameters to Your Query String**

# Query strings basically have two parts:
# 
#  - What follows fhe `?` encodes the actual text to search for, using utf-8 encoding to account for special characters.  This is required.
#  - You can also add additional search parameters, which are encoded by `&`. They dictate what kinds of results are returned.  
#   - For example, a parameter you can use in Twitter's search API is `count`, which tells you how many results to return.  The default is 15, but you can return up to 100.  So if we wanted to search for tweets and return 50 results our query string would look like the following:
#     `https://api.twitter.com/1.1/search/tweets.json?My%20Search%20String&count=50`
#   - You can add as many of these parameters to your string as you'd like.  So for example, if we wanted to include parameters for `count` and `result_type`, we could do the following: `https://api.twitter.com/1.1/search/tweets.json?My%20Search%20String&count=50&result_type=mixed`
#   
# To get the hang of this, try searching for tweets that mention the hashtag `#DeepLearning`, and return 75 results.

# In[5]:


base_url3 = 'https://api.twitter.com/1.1/search/tweets.json'
search3 = '?q=%23DeepLearning&src=typed_query&count=50'

req3 = requests.get(base_url + search, auth=auth).json()
req3


# Try adding a second parameter.  You can find the list here:  https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets

# In[6]:


base_url3 = 'https://api.twitter.com/1.1/search/tweets.json'
search3 = '?q=%23DeepLearning&src=typed_query&count=50&max_id&result_type=mixed'

req3 = requests.get(base_url + search, auth=auth).json()
req3


# ## Section 3: Searching Users

# The last section of the API you'll need to get the hang of before you're let loose is the users API, which allows you to search for users and get their followers, friends, etc, as opposed to tweets which fit a particular criteria.  This part is pretty similar to the advanced lab in class 3, so if you saw how that worked then you shouldn't need much instruction.  
# 
# But if you're seeing this with fresh eyes, you'll want to spend 15-20 minutes to make sure you understand this part.  
# 
# Official documentation can be found here:  https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
# 
# So, as an example, if you want to get a list of someone's followers, you use the base url `https://api.twitter.com/1.1/followers/list.json` and then enter your query string to get a list of that persons followers.  
# 
# List of parameters to use can be found here:  https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference
# 
# One possible parameter to use is `screen_name`, so if you wanted to get a list of someone's followers based on their screen name (the handle that begins with an @), then you would set up your API call to look something like:
# 
# `https://api.twitter.com/1.1/followers/list.json?screen_name=persons_screenname`
# 
# Note that you exclude the `@`.
# 
# **Your turn:** Pull in the list of General Assembly's followers.  General Assembly's handle is `@GA`
# 
# Note that this won't return the whole list of GA's users.  If you want to do that you have to use cursoring:  https://developer.twitter.com/en/docs/basics/cursoring.  This is the topic of your bonus assignment.

# In[7]:


import pprint as pp


# In[8]:


# your answer here
base_url4 = 'https://api.twitter.com/1.1/followers/list.json'
search4 = '?screen_name=sid25393'

req4 = requests.get(base_url + search, auth=auth).json()
pp.pprint(req4)


# In[9]:


pp.pprint(req4)


# In[10]:


base_url5 = 'https://api.twitter.com/1.1/followers/list.json'
search5 = '?screen_name=GA'

req5 = requests.get(base_url + search, auth=auth).json()
pp.pprint(req5)


# In[11]:


pp.pprint(req5)


# ## Section 4: Functions

# This section details the functions you have to write and turn in as part of your homework assignment.  
# 
# Please read the requirements carefully.
# 
# **What you'll turn in:** A `.py` file with all of the functions written.  We should be able to load this into an IDE, run the file, and then call your functions to verify how and if they work. This file should also be properly commented so we can follow your line of reasoning.
# 
# The functions you'll be prompted to write will be defined in the following ways:
# 
#  - **name:** the name of the function
#  - **returns:** what the function should return
#  - **arguments:** arguments to include inside the function in order to specify how it should behave.
#  
#  **Note:** The free API has limitations built into it, so this means from time-to-time you'll only be able to return some of the results from the API.  This is fine.  It's understood and recognized that your functions won't be able to return an entire list of someone's users or other such things, so as long as your work delivers the best it can under present circumstances you'll be in good shape.
#  
#  **Other Note:** Every aspect of the API that you need to use can be found on either of these pages.
#  
#  Search API:  https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
#  
#  Users API: https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference
#  
# **Remarks About Your Final Work**
# 
#  - It's okay if you get stuck somewhere.  If there's one item that you can't figure out and it doesn't quite work right, it's probably best to move on and try other things.  Again, try and explain what you were looking to do.  You'll pass if you give an honest effort.
#  - There's potentially a lot of error handling you could do to verify user input is correct, but you can leave that alone for now.  Just make sure the core purpose of the function works the way it's supposed to.
#  - While you're working on this, it's possible you may bump into your API limits.  Keep this in mind if you have a function that's working, but 45 minutes later it doesn't and you haven't changed anything.  This usually means the data you're getting back from your API calls isn't what it's supposed to be because you've exhausted your limits. We won't hold you to double checking for all of this in your functions.
#  - In the file you turn in, make sure your requests are referencing your API tokens, so that way we can run your file right away.  Ie, make sure somewhere in your script you have a variable at the top that reads `tokens = OAuth1('token1', 'token2', 'token3', 'token4')` so it can be used for your requests inside the file.

# ##### Function 1 (Required)

# **Name:** `find_user`
# 
# **Returns:** dictionary that represents user object returned by Twitter's API
# 
# **Arguments:**
#  - `screen_name`: str, required; Twitter handle to search for.  **Can include the @ symbol.  The function should check for this and remove it if necessary.**
#  - `keys`: list, optional; list that contains keys to return about user object.  If not specified, then function should return the entire user object.  **These only need to be outer keys.** If they are keys nested within another key, you don't have to account for this.
#  
# **To test:** We'll test your function in the following ways:
# 
#  - `find_user('@GA')`
#  - `find_user('GA')`
#  - `find_user('GA', keys=['name', 'screen_name', 'followers_count', 'friends_count'])`

# In[12]:


req5

#print req5['statuses'][0]['user']

pp.pprint(req5['statuses'][0]['user'])


def find_user(screen_name, keys=None):
    for item in req5['statuses']:
        if screen_name==item['user']['screen_name']:
            return item['user']
        
        
    
    #for key, value in  req5['statuses']:
    #    if screen_name == val:
    #        return value


# In[13]:


pp.pprint(find_user('JustBeMentalist',  ['name', 'screen_name', 'followers_count', 'friends_count']))


# ##### Function 2 (Required)

# **Name:** `find_hashtag`
# 
# **Returns:** list of data objects that contain information about each tweet that matches the hashtag provided as input.
# 
# **Arguments:**
#  - `hashtag`: str, required; text to use as a hashtag search.  
#  - `count`: int, optional; number of results to return
#  - `search_type`: str, optional; type of results to return.  should accept 3 different values:
#    - `mixed`:   return mix of most recent and most popular results
#    - `recent`:  return most recent results
#    - `popular`: return most popular results
#    
# **Note:** User should **not** have to actually use the `#` character for the `hashtag` argument.  The function should check to see if it's there, and if not, add it in for them.
# 
# **To Test:**  We'll check your function in the following ways:
#  - `find_hashtag('DataScience')`
#  - `find_hashtag('#DataScience')`
#  - `find_hashtag('#DataScience', count=100)`, and double check the `statuses` key to make sure it contains the right amount of results.
#  - `find_hashtag('#DataScience', search_type='recent/mixed/popular')`

# In[14]:


pp.pprint(req5['statuses'][0]['entities'])


def find_hashtag(hashtag,count=None, search_type=None):
    results=[]
    for item in req5['statuses']:
        if hashtag[0]=="#":
            hashtag=hashtag[1:]
        if hashtag in item['entities']['hashtags']:
            results.append(item['entities'])
        if count > len(results):
            return results
        elif count-1 >=0 :
            return results[:count-1]
            


# ##### Function 3 (Required)

# **Name:** `get_followers`
# 
# **Returns:** list of data objects for each of the users followers, returning values for the `name`, `followers_count`, `friends_count`, and `screen_name` key for each user.
# 
# **Arguments:** 
# 
#  - `screen_name`: str, required; Twitter handle to search for.  **Results should not depend on user inputting the @ symbol.**
#  - `keys`: list, required;  keys to return for each user.  default value: [`name`, `followers_count`, `friends_count`, `screen_name`]; if something else is listed, values for those keys should be returned
#  - `to_df`: bool, required; default value: False; if True, return results in a dataframe.  Every value provided in the `keys` argument should be its own column, with rows populated by the corresponding values for each one for every user.
#  
# **To Test:** We'll test your functions in the following ways:
# 
#  - `get_followers('@GA')`
#  - `get_followers('GA')`
#  - `get_followers('GA', keys=['name', 'followers_count'])`
#  - `get_followers('GA', keys=['name', 'followers_count'], to_df=True)`
#  - `get_followers('GA', to_df=True)`

# In[18]:


pp.pprint(req5['statuses'][0]['entities'])


def get_followers(followers,count=None, search_type=None):
    results=[]
    for item in req5['statuses']:
        if item['entities'][0]['user_mentions']:
            return (item)


# ##### Function 4 (Optional)

# **Name:** `friends_of_friends`
# 
# **Returns:** list of data objects for each user that two Twitter users have in common
# 
# **Arguments:**
# 
#  - `names`: list, required; list of two Twitter users to compare friends list with
#  - `keys`: list, optional; list of keys to return for information about each user.  Default value should be to return the entire data object.
#  - `to_df`: bool, required; default value: False; if True, returns results in a dataframe.
#  
# **To Test:** We'll test your function in the following ways:
# 
#  - `friends_of_friends(['Beyonce', 'MariahCarey'])`
#  - `friends_of_friends(['@Beyonce', '@MariahCarey'], to_df=True)`
#  - `friends_of_friends(['Beyonce', 'MariahCarey'], keys=['id', 'name'])`
#  - `friends_of_friends(['Beyonce', 'MariahCarey'], keys=['id', 'name'], to_df=True)`
#  
# Each of these should return 3 results.  
# 
# **Hint:** The `id` key is the unique identifier for someone, so if you want to check if two people are the same this is the best way to do it.

#  ##### Function 5 (Optional)

# Rewrite the `friends_of_friends` function, except this time include an argument called `full_search`, which accepts a boolean value.  If set to `True`, use cursoring to cycle through the complete set of users for the users provided.  
# 
# The twitter API only returns a subset of users in your results to save bandwidth, so you have to cycle through multiple result sets to get all of the values.
# 
# You can read more about how this works here:  https://developer.twitter.com/en/docs/basics/cursoring
# 
# Basically you have to do a `while` loop to continually make a new request using the values stored in the `next_cursor` key as part of your next query string until there's nothing left to search.
# 
# **Note:** We're using the free API, so we're operating under some limitations.  One of them being that you can only make 15 API calls in a 15 minute span.  You can also only return up to 200 results per cursor, so this means you won't be able to completely search for everyone even if you set this up correctly.
# 
# That's fine, just do what you can under the circumstances.
# 
# **To Test:** To test your function, we'll run the following function calls:
# 
#  - `friends_of_friends(['ezraklein', 'tylercowen'], full_search=True)`
#  
# **Hint:** Chances are you will exhaust your API limits quite easily in this function depending on who you search for.  Depending on how you have things set up, this could cause error messages to arise when things are otherwise fine.  Remember in class 3 when we were getting those weird dictionaries back because our limits were used up?  We won't hold you accountable for handling this inside your function, although it could make some things easier for your own testing.
#        
# Good luck!

# In[16]:


#import twitter 

#api = twitter.Api(consumer_key='NOZHm1aLT1AVmchGbCmiZOAga',
                  #consumer_secret='nPyaYCt8L7ymqGZtU8EqC0a2ypI9aSJgVNIhtoZ0wGsaf3BJw9',
                  #access_token_key='1079981876864008192-AlhO4yOa06oW2sXZpLpWPwnOxEERYS',
                  #access_token_secret='o3E0AsKJfDoTBk77UQYExzOG7E46jPYvpWNGAKsD6lUBY')

#results = api.GetSearch(raw_query = "q=%23DeepLearning&src=recent_search_click")
#results[]

