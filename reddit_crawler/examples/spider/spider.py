from celery import group
from reddit_crawler.examples.spider.tasks import get_subreddit_links

def spider(seedlist):
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

        yield new

def main(seedlist, outfile):
    with open(outfile, 'w') as f:
        for new_names in spider(seedlist):
            for name in new_names:
                print name
                f.write("%s\n" % name)
            f.write("?\n")
