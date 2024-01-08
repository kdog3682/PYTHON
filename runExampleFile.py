from base import *
from next import *


def runExampleFile(lineNumber):
    s = removeStartingComments(read("/home/kdog3682/PYTHON/examples.py"))
    delimiter = "^-{20,} *$"
    lines = s.split("\n")
    index = 0
    for i, line in enumerate(lines):
        if test(delimiter, line):
            index += 1
        if i + 1 == lineNumber:
            break

    items = re.split(delimiter, s, flags=re.M)
    items = map2(items, trim)
    item = items[index]

    if not test("^\w+:", item):
        return executeCode(item)

    config = colonDict(item)
    keys = config.keys()

    for item in ref:
        identifiers = item.get("identifiers")
        fn = item.get("fn")
        transform = item.get("transform")

        if identifiers and not shared(identifiers, keys):
            continue
        if transform and not every(transform.keys(), keys):
            continue

        args, kwargs = getArgsKwargs(fn, config, transform=transform)
        value = fn(*args, **kwargs)
        if value:
            print(value)
        return


def redditFn(subreddit, title, body):
    from reddit_script import Reddit
    title = capitalizeTitle(title)
    subreddit = dictf(env.subreddits, subredditFromUrl)(subreddit)
    body = compose(newlinesToNbsp, prettyProse)
    r = Reddit()
    submission = r.ask(subreddit, title, body)
    print({"submission": submission})
    link = f"http://reddit.com/{submission}"
    ofile(link)


def newlinesToNbsp(s):
    def fn(x):
        # print({"x": x, 'y': x.group(0)})
        # raise 'a'
        length = len(x.group(0))
        if length == 1:
            return "\n\n"
        if length > 1:
            return "\n\n&nbsp;\n\n"

    return re.sub("\n+", fn, s)
    return re.sub("\n(?=\S)\n*", fn, s)


def subredditFromUrl(s):
    return search("/r/(.*?)/", s)


def colonDict(s):
    # util
    items = map2(re.split("^(\w+): *", s.strip(), flags=re.M), trim)
    if items[0] == "":
        items.pop(0)
    config = dict(partition(items))
    return config


def printer(value=None):
    if value:
        blue("Result", value)


def executeCode(code, config={}):
    callableRE = "^[a-zA-Z]\w*(?:\.\w+)*\("
    def bodyReplacer(x):
        name = x.group(1)
        line = x.group(0)
        f = lambda x: f"announce('{x}', {x})"
        payload = map2(split(name, ','), f)
        return f"{line}{newlineIndent(payload)}"

    if not test(callableRE, code, flags=re.M):
        ref = codeLibrary(code)[-1]
        name = ref.get("name")
        params = ref.get("params")
        errorHandlerName = 'errorHandler'
        body = ref.get('text').replace(name, errorHandlerName)
        body = re.sub('^    (\w+(?:, *\w+)*) *= .+', bodyReplacer, body, flags = re.M)
        code += '\n\n' + body + '\n\n'
        callable, top = toCallableFromConfig(name, params, config)
        errorHandlerCallString = callable.replace(name, errorHandlerName)
        callString = stringCall2("printer", callable)
        main = f"""
            try:
                {callString}
            except Exception as e:
                printError(e)
                {errorHandlerCallString}
        """
        code += top + smartDedent(main)

    code = "def main():" + newlineIndent(code) + "main()\n\n"
    # this can be made prettierrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    blue(linebreak)
    print(code)
    blue(linebreak)
    if config.get("stop"):
        blue("Stopping", "No code evaluation")
        return
    exec(code)


ref = [
    {
        "identifiers": ["subreddit"],
        "fn": redditFn,
        "transform": {
            "title": capitalizeTitle,
            "subreddit": dictf(env.subreddits, subredditFromUrl),
            "body": compose(newlinesToNbsp, prettyProse),
        },
    },
    {
        "identifiers": ["code"],
        "fn": executeCode,
    },
]


examplepyfile = "/home/kdog3682/PYTHON/examples.py"

def runExampleFile2(lineNumber):
    s = removeStartingComments(read(examplepyfile))
    regex = "^-{20,} *$"
    lines = s.split("\n")
    start = lineNumber - 1
    index = start
    a = 0
    b = 0
    line = lines[index]
    if test(line, regex):

    while True:


    for i, line in enumerate(lines):
        if test(delimiter, line):
            index += 1
        if i + 1 == lineNumber:
            break

    items = re.split(delimiter, s, flags=re.M)
    items = map2(items, trim)
    item = items[index]

    if not test("^\w+:", item):
        return executeCode(item)

    config = colonDict(item)
    keys = config.keys()

    for item in ref:
        identifiers = item.get("identifiers")
        fn = item.get("fn")
        transform = item.get("transform")

        if identifiers and not shared(identifiers, keys):
            continue
        if transform and not every(transform.keys(), keys):
            continue

        args, kwargs = getArgsKwargs(fn, config, transform=transform)
        value = fn(*args, **kwargs)
        if value:
            print(value)
        return

packageManager(runExampleFile)
