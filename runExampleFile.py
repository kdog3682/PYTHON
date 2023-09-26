from base import *
from next import *

def runExampleFile(lineNumber):
    s = read('/home/kdog3682/PYTHON/examples.py')
    delimiter = '^-{20,} *$'
    lines = s.split('\n')
    index = 0
    for i, line in enumerate(lines):
        if test(delimiter, line):
            index += 1
        if i + 1 == lineNumber:
            break

    items = re.split(delimiter, s, flags = re.M)
    items = map2(items, trim)
    item = items[index]
    config = colonDict(item)

    keys = config.keys()
    for item in ref:

        identifiers = item.get('identifiers')
        fn = item.get('fn')
        transform = item.get('transform')

        if identifiers and not shared(identifiers, keys):
            continue
        elif not every(transform.keys(), keys):
            continue

        args, kwargs = getArgsKwargs(fn, config, transform = transform)
        value = fn(*args, **kwargs)
        if value:
            print(value)
        return

def redditFn(subreddit, title, body):
    from redditscript import Reddit
    r = Reddit()
    return r.ask(subreddit, title, body)

ref = [
    {
        'identifiers': ['subreddit'],
        'fn': redditFn,
        'transform': {
            'title': capitalizeTitle,
            'subreddit': dictf(env.subreddits),
            'body': prettyProse,
        }
    },
]
    
def colonDict(item):
    items = map2(re.split('^(\w+): +', item, flags=re.M), trim)
    items.pop(0)
    config = dict(partition(items))
    return config

runExampleFile(sysArg())
