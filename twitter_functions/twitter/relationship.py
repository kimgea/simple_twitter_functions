'''
Created on 7. okt. 2015

@author: kga



TODO: printout to log.debug
'''

import random
import time
import logging
import tweepy
from datetime import datetime
from datetime import timedelta

import settings
from whitelisted_users import whitelist
import twitter_access


class RelationshipFunctions(object):
    """
        Class holding different follow and unfollow functions
    """
    def __init__(self, screen_name=settings.SCREEN_NAME, key=settings.TWITTER_USER_KEY,
                 secret=settings.TWITTER_USER_SECRET):
        self.api = twitter_access.get_api(key, secret)
        self.screen_name = screen_name
        
        self.followers = []
        self.friends = []    
    
            
    def _gather_followers(self, max_pages=0):
        self.followers = twitter_access.gather_friendships(self.api.followers_ids, self.screen_name, max_pages)
        
    def _gather_friends(self, max_pages=0):
        self.friends = twitter_access.gather_friendships(self.api.friends_ids, self.screen_name, max_pages)    
        
            
    def _gather_friends_followers(self, max_pages=0):
        self._gather_followers(max_pages)
        self._gather_friends(max_pages)
        
        
    def followback(self, max_pages=0):
        """
            Follow back user that follow me, if they are ok
        """
        logging.info(u"check for potential followback")
        friendship_checker = FriendshipChecker(settings.METHOD_FOLLOWBACK)
        
        self._gather_friends_followers(max_pages)
        
        user_ids = set(self.followers).difference(set(self.friends))
        logging.info(u"Possible followback nr: "+unicode(len(user_ids)))
        
        for i in user_ids:
            user = twitter_access.get_user(i, self.api)
            logging.info(u"CHECK: "+unicode(user.screen_name) +u" ____________________________")
            if not friendship_checker.run(user):
                logging.info(u"NOT Follow: "+unicode(user.screen_name))
                time.sleep(60)
                continue
            logging.info(u"Follow: "+unicode(user.screen_name))
            if not settings.SAFE:
                twitter_access.create_friendship(i,self.api)
            time.sleep(60)
        
        
    def unfollow_not_follow_backs(self, max_pages=0):
        """
            Unfollow people not following back, unless user is whitelisted
        """
        logging.info(u"check for users not following back")
        
        self._gather_friends_followers(max_pages)        
        user_ids = set(self.friends).difference(set(self.followers))
        
        if not user_ids:
            logging.info(u"Every one is following back")
            
        for i in user_ids:
            user = twitter_access.get_user(i, self.api)
            if user.screen_name in whitelist:
                time.sleep(60)
                continue
            logging.info(u"unfollow_not_follow_backs: " + unicode(user.screen_name))
            if not settings.SAFE:
                twitter_access.destroy_friendship(i,self.api)
            time.sleep(60)
        
    
    def unfollow(self, max_pages=0):
        """
            Check all friends to se if some is not worth following anymore, then unfollow them
        """
        logging.info(u"check for users to unfollow")
        friendship_checker = FriendshipChecker(settings.METHOD_UNFOLLOW)
        self._gather_friends(max_pages)
        for i in self.friends:
            user = twitter_access.get_user(i, self.api)
            logging.info(u"CHECK: "+unicode(user.screen_name) +u" ____________________________")
            if user.screen_name in whitelist or friendship_checker.run(user):
                time.sleep(60)
                continue
            logging.info(u"unfollow: " + unicode(user.screen_name))
            if not settings.SAFE:
                twitter_access.destroy_friendship(user.screen_name,self.api)
            time.sleep(60)
            
"""       
def follow_followers_followers(self):
    diff = int((len(self.followers)-len(self.friends)) * (random.randrange(80,110,1)*1.0)/100.0)
    user_ids = list(self.followers.union(self.friends))
    #3(4)
    temp_friends=set([])
    limit = 3
    i = 0
    while i < diff:
        if limit + 3 >= 15: #Try to avoit rate limit
            time.sleep(60*120)
            limit = 0
        user_id = random.choice(user_ids)
        if random.randint(0,1) == 0:
            friends_ids = self.api.friends_ids(user_id)
        else:
            friends_ids = self.api.followers_ids(user_id)
        limit+=1
        for friend_id in friends_ids:
            if friend_id in self.followers or friend_id in self.friends or friend_id in temp_friends: 
                continue
            try:
                friend = self.api.get_user(friend_id)
            except:
                continue
            limit+=1
            #TODO: Fix follower/friend ratio... do not follow people with no friends but many folowers
            '''if not friendship_ok_one(friend, d_friends=0, nr_statuses=10, profile_age=0,
                                     q=["book","movie","game","tv","anime","author","write","writing",
                                        "fantasy","fiction","publish","read","watch","scifi",
                                        "nerd","rpg","d&d","comic","geek"]): 
                continue'''
            t = datetime.now()        
            with open("friends_followed.txt","a+") as f:
                f.write(str(t.strftime('%Y%m%d'))+"-"+str(friend_id)+"\n")
            temp_friends.add(friend_id)
            self.api.create_friendship(i)
            limit+=1
            i+=1"""



class FriendshipChecker(object):
    """
        Decides wheter a user should be a friend or not
    """
    def __init__(self, method_type=""):
        """
            @param method_type: "FOLLOWBACK"|"UNFOLLOW"|"" 
        """
        self.FOLLOWER_NR = "followers_nr"
        self.PROFILE_IMAGE = "profile_image"
        self.DESCRIPTION_LENGTH = "description_length"
        self.HAS_STATUS = "has_status"
        self.NR_STATUSES = "nr_statuses"
        self.LAST_ACTIVE = "last_active"
        self.PROFILE_AGE = "profile_age"
        self.QUARIES = "quaries"
        
        self._set_parameters(method_type)
        self._set_rules(method_type)
        
    def _set_parameters(self, method_type):
        self.d_friends = getattr(settings,method_type+"_D_FRIENDSHIP",None)
        self.len_description = getattr(settings,method_type+"_LEN_DESCRIPTION",None) 
        self.profile_image = getattr(settings,method_type+"_PROFILE_IMAGE",None)
        self.nr_statuses = getattr(settings,method_type+"_NR_STATUSES",None)
        self.has_status = getattr(settings,method_type+"_HAS_STATUS",None)
        self.days_active = getattr(settings,method_type+"_DAYS_LAST_ACTIVE",None)
        self.profile_age = getattr(settings,method_type+"_PROFILE_AGE",None)
        self.quaries = getattr(settings,method_type+"_QUARIES",None)
    
    def _set_rules(self, method_type):
        self.rule_active_friendship = getattr(settings,"RULE_FRIENDSHIP_NR_"+method_type,False)
        self.rule_active_description_length = getattr(settings,"RULE_DESCRIPTION_LENGTH_"+method_type,False)
        self.rule_active_status_nr = getattr(settings,"RULE_STATUS_NR_"+method_type,False)
        self.rule_active_has_status = getattr(settings,"RULE_HAS_STATUS_"+method_type,False)
        self.rule_active_last_active = getattr(settings,"RULE_LAST_ACTIVE_"+method_type,False)
        self.rule_active_profile_age = getattr(settings,"RULE_PROFILE_AGE_"+method_type,False)
        self.rule_active_quaries = getattr(settings,"RULE_QUARIES_"+method_type,False)
        self.rule_active_profile_image = getattr(settings,"RULE_PROFILE_IMAGE_"+method_type,False)
        self.rule_active_majority_rule = getattr(settings,"RULE_MAJORITY_RULE_"+method_type,False)
        
    def _full_check(self,user):
        checked = {}
        if self.d_friends != None:
            checked[self.FOLLOWER_NR] = self.check_followers_nr(user,self.d_friends)
        if self.profile_image:
            checked[self.PROFILE_IMAGE] = self.check_profile_image(user)
        if self.len_description != None:
            checked[self.DESCRIPTION_LENGTH] = self.check_description_length(user,self.len_description)
        if self.has_status:
            checked[self.HAS_STATUS] = self.check_statuses(user)
        if self.nr_statuses != None:
            checked[self.NR_STATUSES] = self.check_nr_statuses(user,self.nr_statuses)
        if self.days_active != None:
            checked[self.LAST_ACTIVE] = self.check_last_active(user,self.days_active)
        if self.profile_age != None:
            checked[self.PROFILE_AGE] = self.check_account_age(user, self.profile_age)
        if self.quaries != None:
            checked[self.QUARIES] =  self.check_quaries(user, self.quaries)
        return checked
    
    #################################
    #
    #    _checker functions (rule set) to check if user is ok
    
    def run(self,user):
        """
            Run this to check if user should be a friend or not
        """
        
        checked = self._full_check(user)
        
        #TODO: run rules
        if self.rule_active_description_length:
            if not self.rule_single_check(checked, self.DESCRIPTION_LENGTH):
                return False
        
        if self.rule_active_friendship:
            if not self.rule_single_check(checked, self.FOLLOWER_NR):
                return False
        
        if self.rule_active_has_status:
            if not self.rule_single_check(checked, self.HAS_STATUS):
                return False
        
        if self.rule_active_last_active:
            if not self.rule_single_check(checked, self.LAST_ACTIVE):
                return False
        
        if self.rule_active_profile_age:
            if not self.rule_single_check(checked, self.PROFILE_AGE):
                return False
        
        if self.rule_active_profile_image:
            if not self.rule_single_check(checked, self.PROFILE_IMAGE):
                return False
        
        if self.rule_active_quaries:
            if not self.rule_single_check(checked, self.QUARIES):
                return False
        
        if self.rule_active_status_nr:
            if not self.rule_single_check(checked, self.NR_STATUSES):
                return False
        
        if self.rule_active_majority_rule:
            if not self.rule_majority_rule(checked):
                return False
        
        logging.info(unicode(user.screen_name) + u" - RULE SUCCESS!!!")
        return True
    
    
    ################################
    #
    #    Rules
    
    def rule_majority_rule(self, checked):
        if len([i for i in checked.values() if not i]) > len([i for i in checked.values() if i]):
            logging.info(u" - RULE FAILED: majority rule")
            return False
        logging.info(u" - RULE SUCCESS: majority rule")
        return True
    
    def rule_single_check(self, checked, parameter):
        if not checked.get(parameter,False):
            logging.info(u" - RULE FAILED: single parameter rule - " + unicode(parameter))
            return False
        logging.info(u" - RULE SUCCESS: single parameter rule - " + unicode(parameter))
        return True
    
    ################################
    #
    #    check values from user to se if they are ok  - get facts to be used in rules
    
    def check_followers_nr(self,user,d_friends):
        #IF user follow to many compared to how many followers it has, return false
        if user.followers_count < user.friends_count * d_friends:
            logging.info(unicode(user.screen_name) + u" - Followers FAILED - not enought")
            return False
        logging.info(unicode(user.screen_name) + u" - Followers OK")
        return True
    
    def check_profile_image(self,user):
        #IF user has default profile image, return false
        if user.default_profile_image:
            logging.info(unicode(user.screen_name) + u" - Profile image FAILED - default image")
            return False
        logging.info(unicode(user.screen_name) + u" - Profile image OK")
        return True
    
    def check_description_length(self,user,len_description):
        #IF user has no or to short description, return false
        if len(user.description) < len_description:
            logging.info(unicode(user.screen_name) + u" - Dscription length FAILED - to short")
            return False
        logging.info(unicode(user.screen_name) + u" - Dscription length OK")
        return True
    
    def check_statuses(self,user):
        #IF user last activity to long ago, return false
        if not user.__dict__.get("status",False):
            logging.info(unicode(user.screen_name) + u" - Status FAILED - no status")
            return False
        logging.info(unicode(user.screen_name) + u" - Status OK")
        return True
        
    def check_nr_statuses(self,user, nr_statuses):
        #IF user has to few statuses, return false
        if user.statuses_count < nr_statuses:
            logging.info(unicode(user.screen_name) + u" - Status nr FAILED - to few statuses") 
            return False
        logging.info(unicode(user.screen_name) + u" - Status nr OK")
        return True
    
    def check_last_active(self,user, days_active):
        #IF users has not recently bean active, return False
        if not user.__dict__.get("status",False):
            logging.info(unicode(user.screen_name) + u" - Last active FAILED - No statuses")
            return False 
        if (datetime.now()-user.status.created_at) > timedelta(days=days_active):
            logging.info(unicode(user.screen_name) + u" - Last active FAILED - to long since last update")
            return False
        logging.info(unicode(user.screen_name) + u" - Last active OK")
        return True
    
    def check_account_age(self,user, profile_age):
        #IF profile is to young, return False
        if (datetime.now()-user.created_at) < timedelta(weeks=profile_age):
            logging.info(unicode(user.screen_name) + u" - Account age FAILED - profile to young")
            return False
        logging.info(unicode(user.screen_name) + u" - Account age OK")
        return True
    
    def check_quaries(self,user, quaries):
        #IF quary not in user return False
        for i in quaries:
            if i.lower() in user.description.lower(): 
                logging.info(unicode(user.screen_name) + u" - quary OK")
                return True
        logging.info(unicode(user.screen_name) + u" - Quary FAILED - no quary match")
        return False
        





              
        
    


        







