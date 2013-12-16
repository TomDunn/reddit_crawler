Reddit Crawler
==============

High level
----------

Combines [https://github.com/praw-dev/praw](PRAW) and [http://www.celeryproject.org](Celery) into a barebones "framework" for data collection/processing where [http://www.reddit.com](reddit) is the data source.

That's it really. As of mid-December, the project is tiny as celery and praw do most of the work. 


Installing
----------

At this time, there is not a PyPI package. Clone from github and do:
```bash
sudo python setup.py install
```

Celery requires some sort of managed queue for distributing work. Currently only redis is tested. Because celery is doing all the task distribution, anything that celery supports as a broker should work fine here.

Examples
--------

I've included a simple spidering example. You provide a 'seed' list of subreddits. The spider reads the sidebar of the subreddit, extracts links to other subreddits, then repeats for each found subreddit.

Create a new project directory:
```bash
mkdir my_proj
cd my_proj/
```
Those example config files contain information for a local redis broker. If that is not your setup, pleases edit.

reddit_crawler expects two configuration files in your project:
```
celery_app.py 
praw_config.py
```

then create your run file test.py:
```python
from reddit_crawler.examples.spider.spider import main

main(['funny'])
```

Now it's time to start a worker. The worker in this example makes the API call via PRAW, then parses the sidebar text for link to other subreddits then returns any found subreddits to the caller. The caller takes these subreddit names, filters out any already seen ones, then creates a new task for each unseen subreddit to find more links from them.

Invoke:
```bash
python test.py
```

Roadmap
-------

Coming soon. I would like to add some common collection tasks in the form of chainable tasks.
