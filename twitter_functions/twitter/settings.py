'''
Created on 7. okt. 2015

@author: kga
'''



#############################
#
#    SETTINGS
#

# When safe = True no changes to twitter account is performed
# Queries to twitter account is still done
SAFE = True

#DO NOT TOUCH - TODO: move to constant file?
METHOD_FOLLOWBACK = "FOLLOWBACK"
METHOD_UNFOLLOW = "UNFOLLOW"

#############################
#
#    Logging
#

import logging

LOGNAME = 'example.log'
#LOGNAME = False

if LOGNAME:
    logging.basicConfig(filename=LOGNAME,level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)




################################
#
#    Twitter account info and general api configuration
#
TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""

TWITTER_USER_KEY = ""
TWITTER_USER_SECRET = ""

SCREEN_NAME = ""

# <= 0 THEN scrape all ELSE limit api calls 
MAX_PAGES_INGATHER_FRIENDSHIPS = 0


###################################
#
#    Friendship check parameters - Facts
#

# Check to se if: followers > friends * d_friends
D_FRIENDSHIP = 0.6

# LEN_DESCRIPTION, check if user description has more characters
LEN_DESCRIPTION = 10

#NR_STATUSES: Check to se if  user have more statuses
NR_STATUSES = 300

#Check if user has status updates or not
HAS_STATUS = True

# DAYS_LAST_ACTIVE:  Check if user has been active in these last days
DAYS_LAST_ACTIVE = 5

# PROFILE_AGE: User must be older than x weeks. PROFILE_AGE is in weeks
PROFILE_AGE = 30

# QUARIES is a list of string quaries that is used to check if any of them exist in user profile
# ["nerd", "programming", "tv", "fantasy books"]
#Currently only checks in description... what about checking x latest tweets?
QUARIES = ["book","movie","film","tv","show","serie",
           "author","writer","read","fantasy","anime","manga",
           "action","sci","listening","geek","nerd",
           "drama","fiction"]
 
#PROFILE_IMAGE: to check if user has a profile image
PROFILE_IMAGE=True


# Config parameters fro followback function
FOLLOWBACK_D_FRIENDSHIP = 0.9
FOLLOWBACK_LEN_DESCRIPTION = LEN_DESCRIPTION
FOLLOWBACK_NR_STATUSES = NR_STATUSES
FOLLOWBACK_HAS_STATUS = HAS_STATUS
FOLLOWBACK_DAYS_LAST_ACTIVE = 50
FOLLOWBACK_PROFILE_AGE = PROFILE_AGE
FOLLOWBACK_QUARIES = QUARIES
FOLLOWBACK_PROFILE_IMAGE = PROFILE_IMAGE

# Config parameters for unfollow function
UNFOLLOW_D_FRIENDSHIP = None
UNFOLLOW_LEN_DESCRIPTION = None
UNFOLLOW_NR_STATUSES = None
UNFOLLOW_HAS_STATUS = None
UNFOLLOW_DAYS_LAST_ACTIVE = 100
UNFOLLOW_PROFILE_AGE = None
UNFOLLOW_QUARIES = None
UNFOLLOW_PROFILE_IMAGE = None


###################################
#
#    Friendship rules
#
#    Used to deside whix rules are to be run
#    Rules are hard. If one id fails then all fails

RULE_FRIENDSHIP_NR = False
RULE_DESCRIPTION_LENGTH = False
RULE_STATUS_NR = False
RULE_HAS_STATUS = False
RULE_LAST_ACTIVE = False
RULE_PROFILE_AGE = False
RULE_QUARIES = False
RULE_PROFILE_IMAGE = False

RULE_MAJORITY_RULE = False

#Followback rules
RULE_FRIENDSHIP_NR_FOLLOWBACK = False
RULE_DESCRIPTION_LENGTH_FOLLOWBACK = False
RULE_STATUS_NR_FOLLOWBACK = False
RULE_HAS_STATUS_FOLLOWBACK = True
RULE_LAST_ACTIVE_FOLLOWBACK = False
RULE_PROFILE_AGE_FOLLOWBACK = True
RULE_QUARIES_FOLLOWBACK = True
RULE_PROFILE_IMAGE_FOLLOWBACK = False

RULE_MAJORITY_RULE_FOLLOWBACK = True

#Unfollow rules 
RULE_FRIENDSHIP_NR_UNFOLLOW = False
RULE_DESCRIPTION_LENGTH_UNFOLLOW = False
RULE_STATUS_NR_UNFOLLOW = False
RULE_HAS_STATUS_UNFOLLOW = False
RULE_LAST_ACTIVE_UNFOLLOW = True
RULE_PROFILE_AGE_UNFOLLOW = False
RULE_QUARIES_UNFOLLOW = False
RULE_PROFILE_IMAGE_UNFOLLOW = False

RULE_MAJORITY_RULE_UNFOLLOW = False