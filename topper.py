from twython import Twython
from config import *
import pprint
import requests
requests.packages.urllib3.disable_warnings()

APP_KEY = ckey
APP_SECRET = csecret
OAUTH_TOKEN = atoken
OAUTH_TOKEN_SECRET = asecret

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

list_objects = twitter.show_lists()

list_names = {}
list_ids = {}

def get_lists():
    key = 1
    for list in list_objects:
        list_names[key] = list['name']
        list_ids[key] = list['id']
        key += 1

get_lists()

print "Found your lists!"
pprint.pprint(list_names)

members = []

def print_members():
    which = list_ids[int(raw_input("Which list? "))]
    member_objects = twitter.get_list_members(list_id=which)['users']
    for user in member_objects:
        members.append(user['screen_name'])

print_members()

print "Here are the members:"
pprint.pprint(members)
