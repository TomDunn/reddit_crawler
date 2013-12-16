import praw

reddit = praw.Reddit(user_agent='RedditCrawler example')

print "HERE"

reddit.config.log_requests      = 2
reddit.config.store_json_result = True
