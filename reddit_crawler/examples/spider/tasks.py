from HTMLParser import HTMLParser
from sys import exc_info, stdout
from traceback import print_exception
from urlparse import urlparse

from BeautifulSoup import BeautifulSoup, SoupStrainer

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
        html = HTMLParser().unescape(subreddit.description_html)

        urls = [link['href'] for link in get_links(html)]
        urls = filter(is_reddit_url, urls)

        subreddits = [get_subreddit_from_url(url) for url in urls]
        return [link for links in subreddits for link in links]

    except Exception:
        """
        Any uncaught exception crashes the task requester.
        Just catch and log anything exceptions
        """
        exc_type, exc_value, exc_traceback = exc_info()
        print_exception(exc_type, exc_value, exc_traceback, file=stdout)
        return []
