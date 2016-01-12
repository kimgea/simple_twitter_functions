'''
Created on 7. okt. 2015

@author: kga
'''
"""
    TODO:
        add db storage. Check db before accessing db
"""
import logging
import time
import tweepy

import settings

def get_api(key=settings.TWITTER_USER_KEY,secret=settings.TWITTER_USER_SECRET):
    """
        Get twitter api
        
        args:
            key (str): twitter users api key
            secret (str): twitter users api secret
    """
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(key,secret)
    return tweepy.API(auth)


def get_user(user,api):
    return api.get_user(user)

def create_friendship(user,api):
    api.create_friendship(user)
    
def destroy_friendship(user,api):
    api.destroy_friendship(user)
    




def gather_followers_ids(screen_name, api):
    logging.debug("gather followers_ids")
    return cursor_from_screen_name(api.followers_ids, screen_name,settings.MAX_PAGES_INGATHER_FRIENDSHIPS)
    
def gather_friends_ids(screen_name, api):
    logging.debug("gather friends_ids")
    return cursor_from_screen_name(api.friends_ids, screen_name,settings.MAX_PAGES_INGATHER_FRIENDSHIPS)


def cursor_from_screen_name(model,screen_name,max_pages=0):
    """
        I max_page <= 0 and user has many friends/followers, 
        then this will take a very long time.
        
        args:
            model (api method): methiod to be used to do the calls
            screen_name (str): screen_name of twitter user that is called
            max_pages (int): max pages the Cursor shall call the api.
    """
    logging.debug(u"start coursor: "+unicode(model)+unicode(screen_name)+unicode(max_pages))
    friendships = []
    count = 0
    for page in tweepy.Cursor(model, screen_name=screen_name).pages():
        count += 1
        friendships.extend(page)
        time.sleep(60)
        if count >= max_pages and max_pages > 0:
            logging.debug("break cursor")
            break
    return friendships
