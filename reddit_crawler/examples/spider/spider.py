from celery import group
from reddit_crawler.examples.spider.tasks import get_subreddit_links

def main(seedlist):
    seen = set()
    new  = set(seedlist)

    while len(new):
        new = set([name.lower() for name in new])

        task_group   = group(get_subreddit_links.s(name) for name in new)
        result_group = task_group.apply_async()

        seen = seen | new
        new  = set()

        for result in result_group.iterate():
            names = set([name.lower() for name in result])
            names = names - seen
            new   = new | names

        print "found: " + str(new)

    print "finishing: " + str(seen)
    print str(len(seen))

if __name__ == '__main__':
    main(['Python'])
