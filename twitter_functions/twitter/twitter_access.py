'''
Created on 7. okt. 2015

@author: kga
'''
"""
    TODO:
        add db storage. Check db before accessing db
"""
import time
import tweepy

import settings

def get_api(key=settings.TWITTER_USER_KEY,secret=settings.TWITTER_USER_SECRET):
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(key,secret)
    return tweepy.API(auth)


def get_user(user,api):
    return api.get_user(user)

def create_friendship(user,api):
    api.create_friendship(user)
    
def destroy_friendship(user,api):
    api.destroy_friendship(user)
    
    
def gather_friendships(model,screen_name, max_pages=0):
    """
        NOTE:
                 Hackish way of handeling rate limit... not fully tested
                 5000 retrieced on each page, 1 minute for each page
    """
    friendships = []
    count = 0
    for page in tweepy.Cursor(model, screen_name=screen_name).pages():
        count += 1
        friendships.extend(page)
        time.sleep(60)
        if count >= max_pages and max_pages > 0:
            break
    return friendships
