#/u/GoldenSights
import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import random

import bot_predict

'''USER CONFIGURATION'''

USERNAME  = ""
# This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = ""
# This is the bot's Password. 
USERAGENT = ""
# This is a short description of what the bot does. For example "/u/GoldenSights' Newsletter bot"
# Famous People
MAXPOSTS = 100
# This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
MAXLENGTH = 150
# To avoid bot abuse, do not generate any quotes longer than this many characters.
WAIT = 10
# This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
PATH = 'model/predictor.pkl'
# This is the path to load the ML model from.

'''All done!'''




WAITS = str(WAIT)
try:
    from credentials import credentials #This is a file in my python library which contains my Bot's username and password. I can push code to Git without showing credentials
    USERNAME = credentials['username']
    PASSWORD = credentials['password']
    USERAGENT = credentials['user-agent']
    CLIENT_ID = credentials['client_id']
    CLIENT_SECRET = credentials['client_secret']
except ImportError:
    pass

cutoff = len(USERNAME) + 4

def safer_mark_read(reddit, comment):
    reddit.inbox.mark_read([comment])
    comment.mark_read()

def reply_with_prediction(model, reddit, comment):
    clean_body = clean_comment(comment.body)
    prediction = bot_predict.predict(model, clean_body)
    reply_body = "Is it an insult? Chances are: {}".format(prediction)
    comment.reply(reply_body + '\n\n' + comment_sign_off(prediction))
    print("Reply sent to: ", comment.author)

def clean_comment(body):
    return ' '.join(body.split(' ')[1:]) # strip off bot's name.

def comment_sign_off(comment_rating):
    bad_list = ['nasty', 'cut it out', 'not ok']
    ok_list  = ['borderline', 'passable', 'not sure about this one']
    good_list = ['fine by me', 'kind words']
    if comment_rating > 0.75:
        return random.choice(good_list)
    elif comment_rating < 0.75 and comment_rating > 0.25:
        return random.choice(ok_list)
    else:
        return random.choice(good_list)

def run(reddit, model):
    print("running!")
    for comment in reddit.inbox.unread():
        if 'u/insults_bot' in comment.body:
            print(comment.body)
            reply_with_prediction(model, reddit, comment)
            safer_mark_read(reddit, comment)
        time.sleep(5)

r = praw.Reddit(user_agent=USERAGENT, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)

while True:
    model = bot_predict.load_model(PATH)
    try:
        run(r, model)
    except Exception as e:
        print('An error has occured:', str(e))
    print('Running again in ' + WAITS + ' seconds \n')
    time.sleep(WAIT)
 