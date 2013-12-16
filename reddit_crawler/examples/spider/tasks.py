from HTMLParser import HTMLParser
from urlparse import urlparse

from BeautifulSoup import BeautifulSoup, SoupStrainer
import praw

from reddit_crawler.config import configured_celery_app as celery_app, reddit

def get_links(html):
    links = BeautifulSoup(html, parseOnlyThese=SoupStrainer('a'))
    for link in links:
        yield link

def is_reddit_url(url):
    dn = urlparse(url).netloc

    if dn == '' or dn == 'reddit.com' or dn == 'www.reddit.com':
        return True

def get_subreddit_from_url(url):
    path = urlparse(url).path
    splitted = path.split('/')

    if not 'r' in splitted:
        return []

    if len(splitted) <= splitted.index('r') + 1:
        return []

    display_name = splitted[splitted.index('r') + 1]

    if '+' in display_name:
        return display_name.split('+')

    return [display_name]

@celery_app.task
def get_subreddit_links(name):

    try:
        subreddit = reddit.get_subreddit(name)
        html = subreddit.description_html

        if html is None:
            return []

        html = HTMLParser().unescape(html)
    except (praw.requests.HTTPError, praw.errors.InvalidSubreddit):
        return []

    urls = map(lambda link: link['href'], get_links(html))
    urls = filter(is_reddit_url, urls)
    subreddits = []

    for url in urls:
        subreddits += get_subreddit_from_url(url)

    return subreddits
