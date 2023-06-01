import env
from collections import OrderedDict
#import requests
#import inspect
from base import *

firedir = rootdir + "FIREBASE/"
npmdir = nodedir2023
firedir = rootdir + "FIREBASE/"
playdir = rootdir + "PLAYGROUND/"
resourcedir = rootdir + "Resources2023/"
pipdir = "/usr/lib/python3/dist-packages/pip/"
cm2dir = rootdir + "CM2/"


def to_array(x):
    if isArray(x):
        return x
    return [x]


def is_empty(x):
    if x == 0:
        return False

    if not x:
        return True

    if isinstance(x, (list, tuple, set, frozenset, dict)):
        return not bool(x)

    return len(x) == 0


def early_return(fn):
    def wrapper(*args, **kwargs):
        if is_empty(args[0]):
            print("early return @ empty result")
            return
        result = fn(*args, **kwargs)
        return result

    return wrapper


@early_return
def clipsave(s):
    appendjson("clip.json", [s])


class FileState:
    def __init__(self, file):
        self.file = file
        self.tail = tail(file)
        self.name = removeExtension(self.tail)
        self.extension = getExtension(file)
        self.is_zip = self.extension == "zip"
        self.is_js = self.extension == "js"
        self.is_py = self.extension == "py"
        self.is_html = self.extension == "html"
        pprint(self.file)

    def unzip(self):
        if self.is_zip:
            from zipscript import unzip

            unzip(
                self.file,
            )

    @property
    def data(self):
        try:
            return read(self.file)
        except Exception as e:
            print(str(e))
            return


def smart_manager():

    file = glf()
    ifiz
    return

    def runner(item, key):
        q = item.get(key)
        if q and test("^" + q, getattr(state, key)):
            return True

    keys = ["name", "extension", "tail", "file"]
    for item in smartItems:
        for key in keys:
            if runner(item, key):
                return item["fn"](state)


def appendVim(value, name="temp"):
    value = dumpJson(value)
    s = f"let g:{name} = {value}"
    append("/home/kdog3682/.vimrc", s)


def antichoose(items):
    assert items

    a = prompt2(items)
    if not a:
        return items
    indexes = [int(n) - 1 for n in a.strip().split(" ")]

    store = []
    for i, item in enumerate(items):
        if i not in indexes:
            store.append(item)
    return store


def pyargs(file="base.py"):
    name = getExtension(file) + "args"
    items = antichoose(
        fa(file, "\(([a-z]\w*)\)", filter="<9")
    )
    appendVim(items, name=name)


def toString(s):
    if isFunction(s):
        return inspect.getsource(s)
    return str(s)


def fa(s, r, flags=0, **kwargs):

    s = textgetter(s)
    m = re.findall(r, s, flags=flags)
    if kwargs.get("filter"):
        m = filter(m, kwargs.get("filter"))
    m = unique(m)

    if kwargs.get("choose"):
        m = antichoose(m)

    if kwargs.get("fn"):
        m = map(m, kwargs.get("fn"))

    if kwargs.get("map"):
        m = map(m, kwargs.get("map"))

    if kwargs.get("filter"):
        m = filter(m, kwargs.get("filter"))

    if kwargs.get("append"):
        if kwargs.get("append") == "self":
            appendVariable(dumpJson(m))

    if kwargs.get("clip"):
        clip(m)

    if kwargs.get("save"):
        prompt(m)
        append(currentFile(), join(m))
    pprint(m)
    return m


def map(items, x):
    f = x
    if isString(x):
        x = x.strip()
        f = lambda arg: templater(x, [arg])

    return [f(el) for el in items]


def filter2(items, x=exists):
    f = x
    if isString(x):
        if test("^[<>=]", x):
            f = eval(f"lambda x: len(x) {x}")
        else:
            f = eval(f"lambda x: {x}")

    return [el for el in items if f(el)]


s = """
zip
javascript
python
html
css
"""
t = """
def is_$1(s):
    return getExtension(s) == "$1"
"""

t = """
let g:wpsnippets["$1"]["$2"] = "$3"
"""


def is_javascript(s):
    return getExtension(s) == "js"


def is_zip(s):
    return getExtension(s) == "zip"


def is_css(s):
    return getExtension(s) == "css"


def is_python(s):
    return getExtension(s) == "py"


def is_html(s):
    return getExtension(s) == "html"


class Cache:
    def __init__(self, fallback):
        self.store = {}
        self.fallback = fallback

    def get(self, k):
        m = self.store.get(k)
        if m == None:
            value = self.fallback(k)
            self.store[k] = value
            return value
        print("returning cache")
        return m


def dictf(ref):
    def f(k):
        fn = getattr(ref, k, getattr(ref, "default", None))
        params = count_params(fn)
        return fn, params

    cache = Cache(f)

    def runner(k, v):
        try:
            fn, params = cache.get(k)
            return fn(k) if params == 1 else fn(v, k)
        except Exception as e:
            prompt(error=str(e))
            print("---------------")
            print(str(e))
            print("error")
            dprint(k, v)
            input("throw please")
            input("throw please")
            input("throw please")
            print("---------------")

    return runner


def lines(s, ref=0):
    s = s.strip()
    lines = map(s.split("\n"), trim)
    if test("^ *\w+:", s, flags=re.M):
        lines = map(lines, lambda x: splitonce(x, " *: *"))

    if ref:
        f = dictf(ref)
        lines = [f(*el) for el in lines]

    return lines


str1681989658 = """
    
    margin: 6, 12, 18, 24
    padding: 6, 12, 18, 24
    rel
    abs
    grid: 2,3,4
    directions: 6, 12, 18, 24, -6, -12, -18, -24
"""
# colors: background color outline border-color


s = """

def fn(key, value):
    unit = 'pt'
        case 'margin':
        case 'padding':
            const numbers = getNumbers(b)
            return DIRECTIONS.forEach((d, i) => {
                dirLetter = d[0]
                nameLetter = key[0]
                name = nameLetter + dirLetter
                store.push(name, d + '-')
            })
        case 'colors':
        case 'rel':
        case 'abs':
        case 'grid':
        case 'directions':
"""


def count_params(f):
    data = inspect.signature(f)
    return len(data.parameters)


"pillars.py"


import os


def hashbang(filename):
    assert isfile(filename)
    # Add a hashbang line to the file if it doesn't already have one
    with open(filename, "r") as f:
        first_line = f.readline().strip()

    if not first_line.startswith("#!"):
        print("adding hasbang line")
        with open(filename, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write("#!/usr/bin/env python3\n" + content)

    # Set the execute permission for the file
    os.chmod(filename, 0o755)


def git_push_dir(dir):

    names = gitNames(dir)
    mainCommand = f"""
        cd {dir}
        git add .
        git commit -m "'message'"
        git push
    """

    response = SystemCommand(mainCommand, dir=dir)
    gitData = {
        "success": response.success,
        "error": response.error,
    }

    pprint(gitData)
    pprint(names)


def dprompt(*variables, **kwargs):

    strings = []
    caller = getCaller()
    store = OrderedDict()
    store["caller"] = caller

    for v in variables:
        try:
            vars = (
                inspect.currentframe().f_back.f_locals.items()
            )
            name = [
                v_name
                for v_name, v_val in vars
                if v_val is v
            ][0]
            store[name] = v
        except Exception as e:
            strings.append(v)

    for a, b in kwargs.items():
        store[a] = b

    if strings:
        store["strings"] = strings

    pprint(store)
    return input("")


def gitNames(dir):
    s = SystemCommand("git status --short", dir=dir).success
    pairs = unique(re.findall("(\S+) (\w+(?:\.\w+)+)", s))
    store = [[], []]
    for a, b in pairs:
        if a == "M":
            store[0].append(b)
        else:
            store[1].append(b)
    a, b = store
    return {
        "modified": a,
        "created": b,
    }


def mwrite(inpath, outpath, regex, flags=0):
    inpath = smart_path(inpath)
    outpath = smart_path(outpath, inpath)
    text = read(inpath)
    assert text

    a, payload = mget(regex, text, flags=flags, mode=list)
    assert payload

    append(outpath, payload)
    cfile(inpath, "temp.py")
    write(inpath, a)


def smart_path(file, refpath=0):
    if refpath:
        dir = dirFromFile(refpath)
        file = addExtension(file, getExtension(refpath))
        alert(dir, file)
    else:
        dir = dirFromFile(file)
    return npath(dir, file)


def tesseractExtractText(imageFile):
    from PIL import Image
    import pytesseract

    return pytesseract.image_to_string(
        Image.open(imageFile)
    )


def foo1682173868():
    """
    google -> clip -> delete based on comments = delete
    googleclip
    """

    files = clip()
    chdir(pydir)
    for file in files:
        if file.get("comments").startswith("dele"):
            rfile(file.get("name"))


def get_media(x):

    if isUrl(x):
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            raise Exception("not valid download")
        return r.content
    e = getExtension(x)
    if e:
        if isfile(x):
            return read(x)


def write_media(outpath, data):
    with open(outpath, "wb") as f:
        f.write(data)
        print("successfully wrote to dldir:", outpath)


def download_google_fonts():

    fontdir2023 = dir2023 + "fonts/"
    fontfile = "font.zip"

    for font in fonts:
        font_name = font.replace(" ", "+")
        url = f"https://fonts.google.com/download?family={font_name}"

        dirname = dash_case(font)
        outdir = fontdir2023 + dirname
        dprompt(dirname, outdir)
        data = get_media(url)
        write_media(fontfile, data)
        unzip(fontfile, mkdir(outdir))


def dash_case(s):
    items = re.split("\W|(?=[A-Z]+[a-z])", s)
    return join(filter(items), delimiter="-").lower()


def unzipLatest():
    f = glf()
    readzip(
        f,
        flatten=True,
        outpath=normpath(dldir, removeExtension(tail(f))),
    )

    return flatdir(mostRecent(dldir))


def foo1682177487(r, type=str):
    """
    collectGlobalVariables
    """

    store = {}
    dir_vars = [var for var in globals() if test(r, var)]
    for var in dir_vars:
        value = globals().get(var)
        if isinstance(value, type):
            store[var] = value

    if store:
        appendVariable(dumpJson(store))


def strftime(strife=0):
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    return datetime.now().strftime(strife)


def coerceToObject(x):
    return x if isObject(x) else {"value": x}


def ensure_object(func):
    def decorator(self, obj, *args, **kwargs):
        return func(
            self, coerceToObject(obj), *args, **kwargs
        )

    return decorator


def empty(x, key):
    try:
        return not hasattr(x, key)
    except Exception as e:
        return x == None or len(x) == 0


def info(var):
    var_info = {}
    var_info["class_instance"] = type(var)
    var_info["type"] = type(var).__name__
    var_info["type_str"] = str(type(var))
    var_info["name"] = var.__class__.__name__
    var_info["constructor"] = var.__init__.__func__
    return var_info


def t2s(x):
    return type(x).__name__
    return x.__class__.__name__


def isObjectArray(x):
    return isArray(x) and isObject(x[0])


dateRE = "^#? *(?:\d{6,}|\d\d\D\d\d\D\d\d\d\d)"


def makeRE(s):
    r = s.strip()
    r += "([\w\W]+?)"
    r += "^#? *(?:\d{6,}|\d\d\D\d\d\D\d\d\d\d)"
    return r


def fn(file):
    fileName = filePrompt(
        dir=resourcedir, e="txt", fallback="temp", ref=file
    )
    s = "^04-13-2023 Code for Kids"
    r = makeRE(s)
    s = search(makeRE(s), read(file), flags=re.M).strip()
    write(fileName, s)


def filePrompt(dir="", e="", fallback="temp", ref=0):
    if not dir and ref:
        dir = head(ref)

    if not e and ref:
        e = getExtension(ref)
    name = (
        prompt(dir=dir, message="name for file?")
        or fallback
    )
    name = addExtension(name, e)
    name = os.path.join(dir, name)
    logfile(name)
    return name


def logfile(x):
    if isArray(x):
        s = join(map(x, lambda x: datestamp() + " " + x))
        append("files.txt", s)
        print("append to log file", s)
    else:
        print("logging file", x, "to", "files.txt")
        append("files.txt", datestamp() + " " + x)


r = "https:.*?\.(?:css|js)"
f = lambda x: x.strip() and not test("\\\\u", x)


cmdir = "/home/kdog3682/CM/"


def copy_dir_to_dir(f):
    cfile(cmdir + f, dir2023)


def map(items, fn, *args, filter=1, **kwargs):
    if not items:
        return []

    if isString(fn):
        _key = fn

        arg = toArray(items)[0]
        if isClassObject(arg):
            prompt('aa')
            fn = lambda x: getattr(x, _key)
        elif isObject(arg):
            fn = lambda x: x.get(_key)
        elif "$" in _key:
            fn = lambda x: templater(_key.strip(), [x])
        else:
            fn = lambda x: search(_key, x)

    if isNestedArray(items):
        return [fn(a, b) for a, b in items]

    if isObject(items):
        store = {}
        for k, v in items.items():
            value = fn(k, v)
            if value:
                store[k] = value
            elif filter:
                continue
            else:
                store[k] = v
        return store

    store = []
    for item in toArray(items):
        # print(item)
        try:
            value = fn(item, *args, **kwargs)
            if not (filter and not value):
                store.append(value)
        except Exception as e:
            prompt(item, error="ERROR AT MAP", message=e)
            continue
    return store



def isClassObject(x):
    return type(x) not in env.builtins

def first(x):
    return x.values()[0] if isObject(x) else x[0]


def node_dir_search(*args, root="@codemirror"):
    path = os.path.join(npmdir, root, *args)
    files = os.listdir(path)
    if "dist" in files:
        files = os.listdir(os.path.join(path, "dist"))
    if "index.js" in files:
        path = os.path.join(path, "dist", "index.js")
        return ofile(path)
        cfile(path, os.path.join(dir2023, "commands.js"))


def getdir(*args):
    ff(os.path.join(*args), isdir=1)


def github_content_url(user, repo, file, master="master"):
    base = "https://raw.githubusercontent.com"
    return f"{base}/{user}/{repo}/{master}/{file}"


def textgetter(x):
    if isArray(x):
        return x
    if x == "self":
        return read(currentFile())
    if len(x) > 100:
        return x
    if isGithubUrl(x):
        user, repo, file = x.split("/")[-3:]
        dprompt(user, repo, file)
        url = github_content_url(user, repo, file, "master")
        s = request(url)
        if s == None:
            url = github_content_url(
                user, repo, file, "main"
            )
            s = request(url)
            if s == None:
                raise Exception(
                    "tried master & main -> both none"
                )
        return s
    if isUrl(x):
        return request(x)
    if isfile(normDirPath(x)):
        return normRead(x)
    return x


def request(url):
    r = requests.get(
        fixUrl(url), {"user-agent": env.BROWSER_AGENT}
    )
    if r.status_code == 200:
        return parseJSON(r.text)
    else:
        return None


def removeComments(s):
    r = "^ *(?:<!--|#|//).+\n*"
    return re.sub(r, "", s, flags=re.M)


def npm(s, dir=cm2dir):
    dir = dir2023
    items = (
        split(removeComments(s), "\s+")
        if isString(s)
        else s
    )
    cmd = join(items, delimiter=" ")
    cmd = "npm i " + cmd
    prompt(npmcmd=cmd, dir=dir)
    SystemCommand(cmd, dir=dir)
    printdir(npmdir)


str1682629691 = """
    #@replit/codemirror-vim
    #@codemirror/lang-markdown
    #@codemirror/lang-javascript
    #@codemirror/basic-setup

    #@lezer/common
    #@lezer/lr
    #@lezer/highlight
    #@lezer/generator
    js-yaml
"""

s = """

/mnt/chromeos/MyFiles/Downloads/vite-repro/tokens.js
/mnt/chromeos/MyFiles/Downloads/vite-repro/yaml.js
/mnt/chromeos/MyFiles/Downloads/vite-repro/yaml.terms.js
/mnt/chromeos/MyFiles/Downloads/vite-repro/highlight.js
"""


r = """(\w+)['"]? *[:=]['"]? *(/[^/].+/)"""


s = """

"""


def isGithubUrl(x):
    return "https://github" in x


def ffstring(s):
    ref = {
        "j": "json",
        "c": ["mode", "partition"],
        "res": ["mode", "transfer-to-resources"],
    }

    def f(k):
        val = ref.get(k, k)
        if isArray(val):
            return val
        return val

    kwargs = reduce(split(s, " "), f)
    kwargs["partition"] = True

    ff(dir2023, **kwargs)


# rmdir(cm2dir, 1, 1)

# mkdir()
# printdir(rootdir + 'CM2/node_modules/@codemirror/lang-json/dist')
# printdir(cm2dir)
# npm(clip())
#npm(fa("/home/kdog3682/CM2/cm.raw.js", "(@.*?)['\"]"))

#SystemCommand('npm uninstall @codemirror/closebrackets @codemirror/basic-setup @codemirror/highlight @codemirror/rectangular-selection @codemirror/panel @codemirror/tooltip @codemirror/gutter', dir=rootdir + 'CM2')
#SystemCommand('npm uninstall @codemirror/closebrackets @codemirror/basic-setup @codemirror/highlight @codemirror/rectangular-selection @codemirror/panel @codemirror/tooltip @codemirror/history', dir=rootdir + 'CM2')
#SystemCommand('npm uninstall @codemirror/highlight', dir=rootdir + 'CM2')

s = """

    "@codemirror/autocomplete": "^6.6.0",
    "@codemirror/lang-css": "^6.2.0",
    "@codemirror/lang-html": "^6.4.3",
    "@codemirror/lang-javascript": "^6.1.7",
    "@codemirror/lang-json": "^6.0.1",
    "@codemirror/lang-markdown": "^6.1.1",
    "@codemirror/lang-python": "^6.1.2",
    "@codemirror/language": "^6.6.0",
    "@codemirror/matchbrackets": "^0.19.4",
    "@codemirror/search": "^6.4.0",
    "@codemirror/state": "^6.2.0",
    "@codemirror/theme-one-dark": "^6.1.2",
    "@codemirror/view": "^6.10.1"
"""

#clip(fa(s, "(@.*?)['\"]"))
#cfile('/home/kdog3682/CM2/cm.esm.js', dir2023)


    #@replit/codemirror-vim
#SystemCommand('npm uninstall @codemirror/matchbrackets',  dir=cm2dir)
#ofile(nodedir2023 + '@replit/codemirror-vim/dist/index.js')
#pprint(printDirRecursive(cm2dir + 'node_modules/@codemirror'))
#SystemCommand('npm i @codemirror/commands', dir=cm2dir)
#printdir(cm2dir + 'node_modules/@codemirror/commands/dist')

#mfile('themes.js', 'cm-themes.js')
#mfile('languages.js', 'cm-languages.js')

#ofile(nodedir2023 + '@lezer/highlight/dist/index.js')
#SystemCommand('npm i @codemirror/basic-setup',  dir=cm2dir)
#ofile(nodedir2023 + '@codemirror/basic-setup/dist/index.js')
#ofile(cm2dir + 'node_modules/@codemirror/basic-setup/dist/index.js')
#SystemCommand('npm uninstall @codemirror/basic-setup',  dir=cm2dir)



def review(files=0, move=0, mode=0, **kwargs):
    if not files:
        files = absdir(dir2023)
    if not kwargs:
        kwargs = {
            'js': 1,
            'days': 10,
        }
    files = ff(files, **kwargs)
    if not files:
        print('no files ... early return')
        return 

    removed = []
    moved = []
    saved = []
    os.system("clear")

    for file in files:
        if alwaysDelete(file):
            removed.append(files)
            continue

        a = prompt(fileInfo(file))
        if a == "d":
            removed.append(files)
        elif a:
            saved.append(files)
            
    dprompt(removed, saved)
    clip(saved)
    map(removed, rfile)

#review()
#clip(Partitioner2(ff(js=1, days=5))())

#write('jake.html', read(glf()))

#ofile(budir + 'class.js')
def old(s):
    ofile(budir + s)

#old('utils.js11-08-2022')

#cdir = "/mnt/chromeos/GoogleDrive/MyDrive/CWF/"
#ofile(cdir + 'utils.js04242021')
# a big one

#SystemCommand('npm run dev', dir='/home/kdog3682/2023/vite1')
#SystemCommand('npm i vite --save-dev')
#printdir('/home/kdog3682/2023/vite1')
# /home/kdog3682/2023/vite1/package.json
# /home/kdog3682/2023/vite1/index.html
# /home/kdog3682/2023/vite1/style.css
# /home/kdog3682/2023/vite1/main.js
str1683347537 = """
    
{
  "name": "vite1",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^4.3.2"
  }
}
"""
#SystemCommand('npm run dev', dir='/home/kdog3682/2023/vite1')


#srequest('https://newyork.craigslist.org/brk/edu/d/brooklyn-summer-teaching-position/7618026638.html')
#print(9 ** 0.5)

#print(str(type({})))

def getObservableInitialDataFromLink(url):
    s = request(url)
    r = '<script id="__NEXT_DATA__" type="application/json">([\w\W]+?)</script>'
    m = search(r, s)
    data = parseJSON(m)
    return data
    #s = srequest('https://observablehq.com/@d3/zoomable-circle-packing')

def parseObservableData(data):
    
    data = data.get('props').get('pageProps').get('initialNotebook')
    files = data.get('files')
    nodes = data.get('nodes')
    values = []
    nodes = filter(nodes, lambda x: not test('^md', x.get('value')))
    def sorter(x):
        value = x.get('value')
        return len(value)
        score = 0
        pinned = x.get('pinned')
        id = x.get('id')
        if pinned:
            score += 100

        score += int(id)
        return score
    
    nodes.sort(key=sorter)
    def mapper(node):
        value = node.get('value')
        #if test('a', b):
        return value
    nodes = map(nodes, mapper)
    prompt(nodes)
    prompt(files)

    #files = map(files, 'url')
    #pprint(nodes)
    #pprint(files)


#data = read('observable-data.json')
#parseObservableData(data)
#srequest('https://observablehq.com/@meetamit?tab=notebooks')
#printdir(npmdir)
#ff(dir=firedir, recursion=1, mode='filetable')
#srequest('https://prosemirror.net/examples/schema/')

def fo1(a, b):

    ref = {
        '1': 'standard',
        'del': 'delete',
        'd': 'delete',
        'clear': 'clear',
    }
    m = search('^(?:1|del|d|clear)$', b)
    if m:
        return ['mode', ref[m]]

    m = search('rn (\S+)', b)
    if m:
        if '$' in m:
            m = m.replace('$', a)
        return ['rename', m]

    return ['comment', m]

#clip(data)


def mergejson(file, data):
    if not data: 
        return 
    prev = read(file) or {}
    for k,v in data.items():
        if k in prev:
            if isArray(v):
                prev[k].extend(v)
            else:
                prev[k].update(v)
        else:
            prev[k] = v
    write(file, prev)

def file_table_action():

    def fo2(a, b):
        c, d = fo1(a, b)
        return {'file': a, c: d}

    data=clip()
    r = '^\S+ *(\S+)(?: +(.+))?'
    #data = fa('file-table.txt', r, flags=re.M, fn=fo2)
    prompt(data=data)
    standard = []
    current = []
    for item in data:
        mode = item.get('mode')
        file = item.get('file')
        if mode == 'delete':
            rfile(file)

        elif mode == 'standard':
            standard.append(file)

        elif item.get('rename'):
            mfile(file, item.get('rename'))
        else:
            current.append(file)

    current.sort()
    standard.sort()
    payload = {
        'standard': standard,
        'items': [
            {'date': datestamp(), 'current': current}
        ]
    }
    mergejson('files.json', payload)

#pprint(file_table_action())
#print(isdir('teachingExamples'))
#fa('view-source:https://www.npmjs.com/~marijn?activeTab=packages', r='prosemirror-\w+', clip=1)


prosemirrorNpm = [
    "prosemirror-model",
    "prosemirror-keymap",
    "prosemirror-view",
    "prosemirror-transform",
    "prosemirror-state",
    "prosemirror-example-setup",
    "prosemirror-markdown",
    "prosemirror-inputrules",
    "prosemirror-history",
    "prosemirror-collab",
    "prosemirror-commands",
    "prosemirror-schema-basic",
    "prosemirror-schema-list",
    "prosemirror-schema-table",
    "prosemirror-tables",
]
#import time
#print(int(time.time()))
#1683830000

#npm(prosemirrorNpm)



def prosemirrorFileTable():
    
    def g(dir):
        files = ff(dir, recursive=1, js=1)
        if tail(files[0]) == 'index.es.js':
            return [files[0]]
        return files

    dirs = ff(npmdir, name='^prose')
    dirs = map(dirs, g)
    files = flat(dirs)
    write('pm-file-table.txt', join(files))

#pprint(prosemirrorFileTable())



def parseDiff(dir=dir2023):
    
    new = getNewGitFiles()
    rfile = '^diff --git a/(.*?) b.*\nindex (\w+)\.\.(\w+)'
    cmd = SystemCommand(f""" git diff --word-diff """)
    date = datestamp()
    matches = re.split(rfile, cmd.success, flags=re.M)
    items = partition(filter(matches), 4)
    def parse(x):
        a, b, c, d = x
        prefix = "[\[\{][-+]"
        regex = "^\{\+(?:(?:async )?function[!*]?|def|class|const|var) ([\w\$]+)"
        items = re.findall(regex, d, flags=re.M) or []
        if not items:
            return 

        payload = { 'date': date, 'file': a, 'from': b, 'to': c, 'items': items }
        return payload

    items = filter([parse(x) for x in items])
    for file in new:
        payload = {
            'date': date,
            'file': file,
            'new': True,
        }
        if getExtension(file) == 'js':
            payload['items'] = getFunctionNames(read(file))

        items.append(payload)
    return items

def github_usercontent_url(user, repo, *args, master='master'):
    base = 'https://raw.githubusercontent.com'
    file = '/'.join(args)
    return f"{base}/{user}/{repo}/{master}/{file}"

def manim():
    arg = choose(env.manimToc)
    ofile(github_usercontent_url('3b1b', 'manim', arg[0]))

#pprint(parseDiff())
#printdir(pydir)


def longstamp():
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    return datestamp(strife=strife)

def mdir(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(source_dir):
        source = os.path.join(source_dir, item)
        destination = os.path.join(dest_dir, item)

        if os.path.isfile(destination):
            a = input(f"Do you want to overwrite {destination}? (y/n): ")
            if a.lower() == 'n':
                continue

        shutil.move(source, destination)

    shutil.rmtree(source_dir)

#mdir('/home/kdog3682/Resources2023/MARKDOWN', '/home/kdog3682/MARKDOWN/')
#print(isdir('/home/kdog3682/Resources2023/MARKDOWN'))

markdowndir = '/home/kdog3682/MARKDOWN/'

class Save:
    def __init__(self, file, fallback = {}):
        self.file = file
        self.data = read(self.file) or fallback

    def __enter__(self):
        return self.data

    def __exit__(self, etype, value, traceback):
        if etype:
            return 
        print(self.data)
        #write(self.file, self.data)

def generate_markdown_toc():
    file = 'markdown-toc.json'
    def runner(file):
        print('file', file)

    with Save(file, []) as prev:
        prevFiles = map(prev, 'name')
        g = lambda x: tail(x) not in prevFiles
        files = filter(absdir(markdowndir), g)
        data = map(files, runner)
        prev.extend(data)
        prompt(prev=prev)

#pprint(generate_markdown_toc())
#SystemCommand('npm run dev')

def moveChangeLogFile():
    changelogfile = '/home/kdog3682/2023/changelog.md'
    url = f"{markdowndir}me.{datestamp()}.md"
    mfile(changelogfile, url)


#new = getNewGitFiles()
#print(new)
def push(store, x):
    if x != None:
        store.append(x)


def ignoreFile(name):
    r = '^(?:\W)|license|readme|rc|ignore'
    return test(r, name, flags=re.I)


def createLogger():

    import logging

    logging.basicConfig(filename='logging.txt', level=logging.INFO,
        format='%(message)s')

    logger = logging.getLogger()

    def log(*args):
        s = ' '.join(map(list(args), str))
        return logger.info(s)
    return log

def renameClipToDriveFile():
    newName = prompt('name for drive clip file?')
    cfile(clipfile, drivedir + newName)

def ask_reddit(s):
    import redditscript
    r = redditscript.Reddit()
    try:
        print(r.askString(s))
    except Exception as e:
        print(str(e))
    
def toArray(x):
    if not x:
        return []
    if isArray(x):
        return x
    if isString(x):
        return split(x, "\n")
    return [x]


#pprint(renameClipToDriveFile())
#printdir(nodedir2023)
