import praw

reddit = praw.Reddit(user_agent='RedditCrawler example')

reddit.config.log_requests      = 1
reddit.config.store_json_result = True
