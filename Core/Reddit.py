import praw
import random
import itertools

from prawcore import NotFound

from Config import getToken
from nsfw import isEnabled

def initReddit():
    global r
    r = praw.Reddit(user_agent='Discord Bot', client_id='byorb8K1SwaO1g', client_secret=getToken('Reddit'))

def random_hot_post(subreddit, limit, message):

    try:
        if r.subreddit(subreddit).over18:
            if not isEnabled(message):
                return ":x: Error: Subreddit is NSFW and NSFW is not enabled in this channel. An admin can run the '~togglensfw' command to enable it :x:"
    except NotFound:
        return "Subreddit not found :confounded:"

    submissions = r.subreddit(subreddit).hot(limit=limit)

    if submissions is None:
        return None

    num = random.randrange(1, limit) - 1

    try:
        hot_page = list(itertools.islice(submissions, limit))
        if len(hot_page) == 0:
            return 'Failed to find post matching parameters.'
        random_page = hot_page[num]
    except:
        return None

    if random_page.stickied:
        return random_hot_post(subreddit, limit + 1, message)

    try:
        linked_post = r.submission(url=random_page.url)
        try:
            text = linked_post.title + "\n\n" + linked_post.selftext
            return text[0:2000]
        except:
            return linked_post.title + "\n" + linked_post.url
    except:
        return random_page.title + "\n" + random_page.url


def getCosplay(message, client):
    limit = 30
    try:
        searchTerms = message.content.split(" ")[1]
        searchTerms.replace('_', ' ')
        submissions = r.subreddit('cosplay').search(searchTerms, limit=limit)

    except IndexError:
        submissions = r.subreddit('cosplay').hot(limit=limit)

    num = random.randrange(1, limit) - 1

    try:
        hot_page = list(itertools.islice(submissions, limit))
    except:
        return 'There was an error retrieving a post :cty:'

    if len(hot_page) == 0:
        return 'Failed to find post matching parameters.'
    try:
        random_page = hot_page[num]
    except:
        return 'Failed to find a post matching parameters.'

    if random_page.stickied:
        return getCosplay(message, client)

    return random_page.title + "\n" + random_page.url

def getCosplayGirl(message, client):
    limit = 30

    try:
        searchTerms = message.content.split(" ")[1]
        searchTerms.replace('_', ' ')
        submissions = r.subreddit('cosplaygirls').search(searchTerms, limit=limit)

    except IndexError:
        submissions = r.subreddit('cosplaygirls').hot(limit=limit)

    num = random.randrange(1, limit) - 1

    try:
        hot_page = list(itertools.islice(submissions, limit))
    except:
        return 'There was an error retrieving a post :cty:'

    if len(hot_page) == 0:
        return 'Failed to find post matching parameters.'
    try:
        random_page = hot_page[num]
    except:
        return 'Failed to find a post matching parameters.'

    if random_page.stickied:
        return getCosplay(message, client)

    return random_page.title + "\n" + random_page.url


def random_top_post(subreddit, message, limit):
    try:
        if r.subreddit(subreddit).over18:
            if not isEnabled(message):
                return ":x: Error: Subreddit is NSFW and NSFW is not enabled in this channel. An admin can run the '~togglensfw' command to enable it :x:"
    except NotFound:
        return "Subreddit not found :confounded:"

    submissions = r.subreddit(subreddit).top(limit=limit)

    if submissions is None:
        return None

    num = random.randrange(1, limit) - 1

    try:
        top_page = list(itertools.islice(submissions, limit))
        if len(top_page) == 0:
            return 'Failed to find post matching parameters.'
        random_page = top_page[num]
    except:
        return None

    if random_page.stickied:
        return random_hot_post(subreddit, limit + 1, message)

    try:
        linked_post = r.submission(url=random_page.url)
        try:
            text = linked_post.title + "\n\n" + linked_post.selftext
            return text[0:2000]
        except:
            return linked_post.title + "\n" + linked_post.url
    except:
        return random_page.title + "\n" + random_page.url
