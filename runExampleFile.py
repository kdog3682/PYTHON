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
    # if not test('^code:', item):
        # a, b = splitonce(item, '\n(?=(?:def |class |from \w+ import|import |\w+ = ))')
        # config = colonDict(a)
        # if b:
            # config['code'] = b
    # else:
    config = colonDict(item)

    if not config:
        red('Error')
        return pprint({"item": item, "itemLength": len(items), 'ln': lineNumber, 'index': index})

    keys = config.keys()
    for item in ref:
        identifiers = item.get('identifiers')
        fn = item.get('fn')
        transform = item.get('transform')

        if identifiers and not shared(identifiers, keys):
            continue
        if transform and not every(transform.keys(), keys):
            continue

        args, kwargs = getArgsKwargs(fn, config, transform = transform)
        value = fn(*args, **kwargs)
        if value:
            print(value)
        return

def redditFn(subreddit, title, body):
    from redditscript import Reddit
    r = Reddit()
    id =  r.ask(subreddit, title, body)
    print({"id": id})
    link = f"http://reddit.com/{id}"
    ofile(link)


def newlinesToNbsp(s):
    def fn(x):
        # print({"x": x, 'y': x.group(0)})
        # raise 'a'
        length = len(x.group(0))
        if length == 1:
            return '\n\n'
        if length > 1:
            return '\n\n&nbsp;\n\n'
    return re.sub('\n+', fn, s)
    return re.sub('\n(?=\S)\n*', fn, s)

def subredditFromUrl(s):
    return search('/r/(.*?)/', s)

def colonDict(item):
    # util
    items = map2(re.split('^(\w+): *', item.strip(), flags=re.M), trim)
    if items[0] == '':
        items.pop(0)
    config = dict(partition(items))
    return config

def executeCode(code, config):
    callableRE = "^[a-zA-Z]\w*(?:\.\w+)*\("
    if not test(callableRE, code, flags = re.M):
        ref = codeLibrary(code)[-1]
        name = ref.get('name')
        params = ref.get('params')
        callable = toCallableFromConfig(name, params, config)
        code += '\n\n' + callable

    code = 'def main():' + newlineIndent(code) + 'main()\n\n'
    blue(linebreak)
    print(code)
    blue(linebreak)
    if config.get('stop'):
        blue('Stopping', 'No code evaluation')
        return 
    exec(code)

ref = [
    {
        'identifiers': ['subreddit'],
        'fn': redditFn,
        'transform': {
            'title': capitalizeTitle,
            'subreddit': dictf(env.subreddits, subredditFromUrl),
            'body': compose(newlinesToNbsp, prettyProse),
        }
    },
    { 'identifiers': ['code'], 'fn': executeCode, },
]


    

packageManager(runExampleFile)
