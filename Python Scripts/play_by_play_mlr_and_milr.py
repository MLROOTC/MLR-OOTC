import praw
from dhooks import Webhook
import datetime
import time

#  Enter the search terms for your MLR and MiLR team in the quotes, for example 'Oakland A' or 'Philadelphia B'.
search_term_mlr = ''
search_term_milr = ''

#  Create a webhook in your server by going to Server Settings > Integrations > Webhooks, and create a new Webhook. Set
#  the name and channel, and add an icon if you'd like. Click the Copy Webhook URL button and paste it below inside the 
#  quotes.
webhook_MLR = Webhook('')
webhook_MiLR = Webhook('')

#  To generate a client ID and secret, go here: https://www.reddit.com/prefs/apps scroll all the way to the bottom, and
#  hit the create an app button. Enter something for name and redirect URL, and make sure the script radio button is
#  selected. Hit the create app button, and then paste the client ID and secret below. The user_agent string literally 
#  just needs to have some text in it, does not matter what. 
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent=''
)

# Don't change anything after here.


def parse_comments():
    for comment in reddit.subreddit('fakebaseball').stream.comments(skip_existing=True):
        update = '**/u/%s on [%s](<https://www.reddit.com%s>)**' % (comment.author, comment.link_title, comment.permalink)
        update += '```%s```' % comment.body
        update += '*Created at %s*' % (datetime.datetime.fromtimestamp(comment.created))
        if search_term_mlr.lower() in comment.link_title.lower():
            webhook_MLR.send(update)
        elif search_term_milr.lower() in comment.link_title.lower():
            webhook_MiLR.send(update)


while True:
    try:
        parse_comments()
    except Exception as e:
        print(e)
        time.sleep(60)
    else:
        time.sleep(360)
