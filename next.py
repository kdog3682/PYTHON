hskjsondictfile = '/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-dict.json'
import env
import time
import os
import traceback
import sys
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
    def getZipFiles(self):
        from zipscript import getZipFiles
        return getZipFiles(self.file, self.head)
    
    def __repr__(self):
        return self.file
    
    def __init__(self, file):
        self.file = file
        head, tail = headAndTail(file)
        self.head = head
        self.tail = tail
        self.name = removeExtension(self.tail)
        self.extension = getExtension(file)
        self.is_zip = self.extension == "zip"
        self.is_js = self.extension == "js"
        self.is_py = self.extension == "py"
        self.is_html = self.extension == "html"

    def remove(self):
        rfile(self.file)
    
    def unzip(self, dest=0, **kwargs):
        if not self.is_zip:
            return 

        from zipscript import unzip
        files = unzip(self.file, dest or self.head)
        if kwargs.get('save'):
            save(files)

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
    _promptOnce = kwargs.pop('promptOnce', None)
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
    for i, item in enumerate(toArray(items)):
        try:
            value = fn(item, *args, **kwargs)
            if not (filter and not value):
                if i == 0 and _promptOnce:
                    promptOnce(value, _promptOnce)
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


#os.system('''node --experimental-modules -e "import { fooga } from './utils.js'; console.log(fooga('a', 'b'));"''')
#parseDiff()



def removeSmallFiles(files):
    for file in files:
        if isfile(file) and fsize(file) < 50:
            rfile(file)

def parseDiff(dir):

    result = SystemCommand('git status --short', dir=dir)
    r = '^ *(\?\?|M) (.+)'
    m = re.findall(r, result.success, flags=re.M)
    if not m:
        return 

    modified = []
    created = []
    for a,b in m:
        if removable(b):
            continue

        if a == '??':
            created.append(b)
        else:
            modified.append(b)

    date = datestamp()
    payload = {'date': datestamp()}
    if modified: payload['modified'] = modified
    if created: payload['created'] = created
    payload['directory'] = dir

    pprint(payload)
    appendjson('/home/kdog3682/2023/git-data3.json', payload, mode=list)

def gitPush(dir):

    mainCommand = f"""
        cd {dir}
        git add .
        git commit -m "'autopush'"
        git push
    """

    parseDiff(dir=dir)
    SystemCommand(mainCommand, dir=dir, printIt=1)

def removable(f):
    if isfile(f) and fsize(f) < 50:
        rfile(f)
        return True

def FixGitCache():
    
    SystemCommand('''
        git rm --cached -r
        git add .
    ''')


#FixGitCache()




def moveRecentlyDownloadedFileToDrive(name):

    def drivepath(file, ext):
        return f"{drivedir}{name}.{timestamp()}.{getExtension(ext)}"

    file = glf(dldir)
    outpath = drivepath(name, ext=file)
    dprompt(outpath)
    mfile(file, outpath)

#moveRecentlyDownloadedFileToDrive('chrome-history')

def cleanupDldir():
    chdir(dldir)
    files = os.listdir()
    
    print(files)
    #cleanupDldir()

    #Do it via javascript and server ... yes.

def foo():
    print('hi')


class Silence:
    def __init__(self, silencer = True):
        self.stdout = sys.stdout
        self.silencer = silencer

    def __enter__(self):

        class NullWriter:
            def write(self, s):
                pass

            def flush(self):
                pass
        
        if self.silencer:
            sys.stdout = NullWriter()

    def __exit__(self, etype, value, traceback):
        sys.stdout = self.stdout


def sysArgs():
    base = sys.argv[1:]
    length = len(base)
    if length == 0:
        return ['', []]
    if length == 1:
        return [base[0], []]
    return [base[0], base[1:]]

def runModule(module=0):
    
    data = None
    with Silence(True):
        arg, args = sysArgs()

        if not arg:
            return

        fn = None
        if module:
            if hasattr(module, arg):
                fn = getattr(module, arg)
        else:
            fn = globals().get(arg, None)

        if fn:
            try:
                data = {'success': fn(*args)}
            except Exception as e:
                error = {
                    "type": type(e).__name__,
                    "message": str(e),
                    "stack": traceback.format_exc()
                }
                data = {'error':  error}

    return json.dumps(data)


def backupFolder(dir):
    dir = dirgetter(dir)
    for file in absdir(dir):
        cfile(file, budir)

#backupFolder('clips')
def seeBackup(file):
    file = f"{budir}{file}.backup"
    print(read(file))

#seeBackup('null.js')
#printdir(budir)


def driveWrite(file, s):
     write(drivedir + addExtension(file, 'py'), s)

class DropBox:
    def __init__(self):
        from dropbox.files import WriteMode
        from dropbox import Dropbox
        self.dropbox = Dropbox(env.dropboxtoken)
        self.mode=WriteMode('overwrite')

    def push(self, file):
        path = '/' + tail(file)
        with open(npath(file), 'rb') as f:
            r = self.dropbox.files_upload(f.read(), path, mode=self.mode)
            return r

    def pull(self, file):
        path = '/' + tail(file)
        meta, response = self.dropbox.files_download(path)
        return response.content.decode('utf-8')


def npath(dir=0, file=0):
    if isArray(file):
        return map2(file, lambda x: npath(dir, x))
    if not dir:
        return file
    elif not file:
        return npath(dirFromFile(file), file)
    if isfile(dir):
        if not getExtension(file):
            file = addExtension(file, getExtension(dir))
        dir = head(dir)
    return os.path.join(dirGetter(dir), tail(file))

def gitCloneAndMove(repoUrl, move=1):
    repoUrl = search('.*?github.com/[\w-]+/[\w-]+', repoUrl)
    name = repoUrl.split('/')[-1]
    #dprompt(repoUrl, name)
    SystemCommand(f'''
        cd {dldir}
        git clone {repoUrl}
    ''')


    dir = npath(dldir, name)
    save(dir)

    if not move:
        return 
    if not isdir(dir):
        return 

    src = os.path.join(dir, 'src')
    if not isdir(src):
        src = dir
    files = getFiles(src)
    newdir = f'Git Repo - {name}'
    newdir = npath(dldir, newdir)
    shutil.move(src, newdir)
    rmdir(dir, force=1)

#gitCloneAndMove('https://github.com/sagalbot/vue-select/blob/master/src/scss/modules/_spinner.scss')

def getFiles(dir, **kwargs):
    recursive = kwargs.pop('recursive', False)
    def runner(dir):
        for file in absdir(dir):
            if isIgnoredFile2(file):
                continue
            elif isfile(file) and checkpoint(file):
                store.append(file)
            elif recursive and isdir(file):
                runner(file)

    store = []
    checkpoint = checkpointf(**kwargs)
    runner(dirGetter(dir))
    return store

def isIgnoredFile2(file):
    name = tail(file)
    ignore = [
        "vosk-api",
        "__pycache__",
        "node_modules",
        ".git",
        ".gitignore",
    ]
    ignoreRE = "^(?:\W)"
    recursiveIgnoreRE = "^(?:LICENSE|README\.[mM][dD])$"

    if fsize(file) < 100:
        return True
    if name in ignore:
        return True
    if test(ignoreRE, name):
        return True

def c2(s):
    write('clip.js', s)

#c2(getFiles(npath(dldir, 'Git Repo - vue-select')))



class NYTimes:
    def __init__(self):
        pass

    def articlesearch(self, topic, **kwargs):
        base = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
        page = kwargs.get('page', 0)
        curl = f'{base}q={topic}&api-key={env.nytimesApiKey}&page={page}'
        data = request(curl)
        docs = data.get('response').get('docs')
        map(docs, ['abstract', 'web_url as url', 'pub_date as date', 'byline.original', 'word_count'])


#ny = NYTimes()
#clip(ny.articlesearch('food'))
#clip(request())



def incrementalName(s, dir = 'drive'):
    override = 0
    if s.endswith('!'):
        s = s[:-1]
        override = 1
    front = removeExtension(s)
    e = getExtension(s)
    d = dirGetter(dir)
    count = 1
    while count < 50:
        name = os.path.join(d, f'{front} {count}.{e}')
        if override:
            return name
        if not isfile(name): return name
        count += 1

def dirGetter(dir=None):
    if not dir:
        return os.getcwd()
    value = env.dirdict.get(dir, dir)
    assert isdir(value)
    return value


def foo1689558041(f):
    mfile(f, incrementalName(f))

#foo1689558041('changelog.md')
s='''NotoColorEmoji.ttf Sohne-Halbfett.otf'''
def moveToActiveDir(s):
    files = map(xsplit(s), lambda x: npath(dirGetter('dl'), x))
    for file in files:
        mfile(file, dir2023)

#pprint(moveToActiveDir(s))

def rpw(file, f):
    write(file, f(read(file)))

def relpath(s):
    prefix = ''
    return s.replace('/home/kdog3682/2023/', prefix)

def foo1689563342(s):
    def parser(x):
        f = x.group(0)
        name = addExtension(d[f], getExtension(f))
        outpath = npath('fonts', name)
        mfile(f, outpath)
        return relpath(outpath)
    r = 'font-family: \'(.*?)\'[\w\W]+?([\w-]+\.woff2)'
    d = reverse(dict(findall(r, s)))
    s = re.sub('[\w-]+\.woff2', parser, s)
    return s



#printdir(dirGetter('fontdir'))

#rpw('material-icons.css', foo1689563342)

def headAndTail(s):
    a, b = os.path.split(s)
    if a == '':
        a = '/home/kdog3682/2023'
    return a, b

def unzipfilestodir(outdir):
    files = getFiles('dl', zip=1, hours=1, recursive=0)
    prompt(files)
    for file in files:
        f = FileState(file)
        f.unzip(outdir)
        f.remove()

#printdir(fontdir)
#files = getFiles('cwd')
#clip(files)


def extractAZipFile(file):
    f = FileState(glf())
    f.unzip(trashdir)
    g = trashdir + file
    mfile(g, dir2023)
    return file

#clip(read('conversations.json')[0])

def fo():
    def f(a):
        message = a.get('message')
        if not message:
            return 

        role = message.get('author').get('role')
        if role == 'assistant':
            parts = message.get('content').get('parts')
            s = join(parts)
            r = '```(\w+)\s+([\w\W]+?)```'
            m = re.findall(r, s)
            store.extend(m)

    store = []
    data = list(clip().get('mapping').values())
    map(data, f)
    #pprint(store)

    chromeExtensionName = 'myFirstExtension'
    dir = mkdir(dldir + chromeExtensionName)
    chdir(dir)
    for extension, contents in store:
        if extension == 'js':
            write('background.js', contents)

        if extension == 'json':
            write('manifest.json', parseJSON(contents))
        #'/mnt/chromeos/MyFiles/Downloads/myFirstExtension/manifest.json'
        #'/mnt/chromeos/MyFiles/Downloads/myFirstExtension/background.js'

#fo()

#gitCloneAndMove('https://github.com/an-object-is-a/chrome-ext-mv3-how-to', move=0)

def linKeSong():
    def getUrl(n):
        return "jjwxc.net/onebook.php?novelid=2337210&chapterid={n}"

    def parser(n):
        url = fixUrl(getUrl(n))
        s = request(url)
        c2(s)

    parser(1)

#linKeSong()
def oc():
    ofile('clip.js')

class LinKeSong:
    def __init__(self):
        pass

    def run(self):
        f = lambda x: int(findall('\d+(?!\))', x)[-1])
        items = sort(mostRecent(dldir, 9), f)
        store = []

        for i,item in enumerate(items):
            if i == 0:
                store.append(self.foo1689880202(item))
            else:
                store.append(self.foo2(item))

        clip(store)

    def openLinKeSong(self):
        items = list(range(1, 10, 1))
        urls = map(items, lambda x: fixUrl(f"jjwxc.net/onebook.php?novelid=2337210&chapterid={x}"))
        for url in urls:
            time.sleep(1)
            ofile(url)

        
    def parse(self, m):
        def f(x):
            return '\n' * len(findall('br', x.group(0))) 
        
        m = re.sub('[\t ]*(?:<br/?>\s*)+[\t ]*', f, m)
        m = re.sub('。 *', '. ', m)
        m = re.sub('”', '"', m)
        m = re.sub('“', '"', m)
        m = re.sub('“', '"', m)
        m = re.sub(' +"', '"', m)
        m = re.sub('^[\t ]+', '', m, flags=re.M)
        return m
    
    def foo1689880202(self, file):
        s = read(file)
        r = 'class="readsmall".*?>[\w\W]+?</div>\s*([\w\W]+?)<div'
        m = search(r, s)
        return {
            'title': 'aaaaaaaaaaaaaaaaaaaaaa',
            'text': self.parse(m),
        }

    def todohsk():
        hskjsonfile = "/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-master.json"
        data = read(hskjsonfile)
        store = {}
        
        for item in data:
            id = item.get('id')
            hanzi = item.get('hanzi')
            pinyin = item.get('pinyin')
            translations = item.get('translations')[0]

    def remove(self):
        files = getFiles('dl', recursive=0, name='jjwxc')
        rfiles(files)
    def check(self, n=0):
        a = clip()[n]
        if isObject(a):
            a = a.get('text')
        self.a(a)
    def a(self, a):
        write('a.txt', dumpJson(a))
        ofile('a.txt')
    

    def gpt(self):
        input_string = "<h2>舌尖上的吻</h2><br/></div> <div "
        chinese_pattern = r'[\u4e00-\u9fff]+'
        chinese_chars = re.findall(chinese_pattern, input_string)
        print(chinese_chars)  # Output: ['舌尖上的吻']
        return chinese_chars

    def foo2(self, file):
        r = r'<h2>([\u4e00-\u9fff]+.*?)<[\w\W]+?([\u4e00-\u9fff][\w\W]+?)</?div'
        s = search(r, read(file))
        assert(s)
        a, b = s 
        b = self.parse(b)
        return {
            'title': a,
            'text': b
        }

    def pinyin(self):
        from pypinyin import pinyin
        items = clip()
        for item in items:
            s = item.get('text')
            pinyinText = flat(pinyin(s))

            s = item.get('title')
            pinyinTitle = flat(pinyin(s))
            return 

    def jieba(self):

        import jieba
        from pypinyin import pinyin

        out = []
        items = clip()
        seen = set()

        for item in items:
            s = item.get('text')
            words = list(jieba.cut(s))
            titleWords = list(jieba.cut(item.get('title')))
            store = []
            out['body'] = words
            out['title'] = titleWords 
            out['vocabulary'] = store

            for i, item in enumerate(words):
                if not isChinese(item):
                    continue

                if len(item) == 2 and item[0] == '地':
                    item = item[1]

                if item in seen:
                    continue

                p = flat(pinyin(item))
                store.append({'index': i, 'pinyin': p, 'hanzi': item})
                seen.add(item)

        write('linKeSongData.json', out)
        

chineseRE = r'[\u4e00-\u9fff]+'
notChineseRE = r'[^\u4e00-\u9fff]+'
def isChinese(s):
    return test(chineseRE, s)
    

#LinKeSong().check(2)


def foo(self):
    return 'export default ' + dumpJson(out)
#write('a.txt', clip()[0].get('text'))

#LinKeSong().jieba()

def copyClipFileToDrive(name):
    name = npath('drive', name)
    cfile('clip.js', name)
    save(name)

def doStoryOfYangxiPalace():

    outpath = npath('jsondrive', 'storyOfYangxiPalace.jieba.json')
    touched = 0

    def parser(file):
        nonlocal touched
        episode = search('S01E(\d+)', file)
        if episode:
            episode = int(episode)
        else:
            return 

        print('doing file', file)
        lines = linegetter(file, fn=jieba.cut)

        if not touched:
            touched = 1

        return {
            'episodeNumber': episode,
            'lines': lines,
        }

    file = "drive-download-20230719T171808Z-001.zip"
    file = FileState(npath('trash', file))
    translations = file.getZipFiles()
    jieba = Jieba()
    payload = map2(translations, parser, sort='episodeNumber')
    try:
        write(outpath, payload)
    except Exception as e:
        clip(payload)
    

def skipPrompt(*args, **kwargs):
    
    import inspect
    message = None
    names = []

    for i, arg in enumerate(args):
        if i == 0 and arg != None:
            return 
        else:

            try:
                vars = inspect.currentframe().f_back.f_locals.items()
                els = [v_name for v_name, v_val in vars if v_val is arg]
                name = els[0]
                names.push(name)
            except Exception as e:
                message = arg
        
    printItems = [ f"{names[0]} does not exist" ]
    if message: printItems.append(message)
    if kwargs: printItems.append(kwargs)
    print(*printItems)
    return input('')

def initializeGlobalVariable(key=0):
    global promptOnceTouched
    try:
        if promptOnceTouched:
            print('already touched early return')
            return 
        promptOnceTouched = True
        return True
    except Exception as e:
        if (type(e) == NameError):
            promptOnceTouched = True
            return True
        else:
            raise e
        

def promptOnce(x, mode=0):
    if initializeGlobalVariable('promptOnceTouched'):
        prompt(x, mode)



class Jieba:
    def __init__(self, convert=0):
        import jieba
        from pypinyin import pinyin

        self.jieba = jieba
        self.ref = read(hskjsondictfile)
        self.pinyin = lambda x: ''.join(flat(pinyin(x)))
        self.watcher = Watcher()
        self.count = 0

        if convert:
            from opencc import OpenCC
            cc = OpenCC(convert)
            self.simpliefied = lambda x: cc.convert(x)


    def cut(self, s, timestamp=0):
        self.count += 1

        store = []
        tokens = self.jieba.cut(s.strip())

        for i, item in enumerate(tokens):
            data = {
                'index': i,
                'hanzi': item,
            }

            if not isChinese(item):
                type = 'punctuation'
                data['type'] = type
                store.append(data)
                continue

            data['pinyin'] = self.pinyin(item)

            if len(item) == 2 and item[0] == '地':
                type = 'adjectiveConversion'
                key = item[1]
                if key not in self.watcher:
                    data['new'] = True
                store.append(data)
                continue

            data['new'] = item not in self.watcher
            data['type'] = 'hanzi'
            store.append(data)

        chinesePinyin = ''
        for item in store:
            if item.get('type') == 'punctuation':
                chinesePinyin = chinesePinyin.rstrip()
                chinesePinyin += item.get('hanzi')
            else:
                chinesePinyin += item.get('pinyin')
                chinesePinyin += ' '

            if item.get('new'):
                ref = self.ref.get(item.get('hanzi'))
                if ref:
                    item['level'] = ref['level']
                    item['translation'] = ref['translations'][0]

        data = {
            'tokens': store,
            'hanzi': s,
            'pinyin': chinesePinyin.strip(),
        }
        if timestamp:
            data['timestamp'] = timestamp
        return data
        return store

def makehsk():
    """ asdfd2 """
    hskjsonfile = "/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-master.json"
    path = npath(hskjsonfile, 'hsk-dict')
    dprompt(path)
    data = read(hskjsonfile)
    store = {}
    for item in data:
        t = item.get('translations')[0]
        store[item.get('hanzi')] = item

    write(path, store)
    save(path, mode='python')
    return store
    
class Watcher:
    def __init__(self):
        self.seen = set()
    def __contains__(self, x):
        if x in self.seen:
            return True
        else:
            self.seen.add(x)
            return False


#pprint(Jieba().cut("我们喜欢吃饭。你呢？我们吃地笑"))

def help(fn):
    return fn.__doc__

#print(help(makehsk))
#pprint(choose(alist))
#pprint(dollarPrompt(['$1 aaa $1']))
#When you miss the timing ... the timing is not recoverable ...
#https://book.douban.com/subject/24526949/


def zokarious():
    write(npath('drive', 'foo.js'), 'aaa')

def map2(items, fn, **kwargs):
    store = []
    for index, originalItem in enumerate(items):
        try:
            value = fn(originalItem)
            if value == None:
                continue
            store.append(value)
        except Exception as error:
            errorPrompt(index, originalItem, error)
    if kwargs.get('sort'):
        return sort(store, kwargs.get('sort'))
    return store
        

def errorPrompt(*args, **kwargs):
    
    import inspect
    caller = getCaller()
    message = 'Error at: ' + caller
    for i, arg in enumerate(args):
        try:
            vars = inspect.currentframe().f_back.f_locals.items()
            e = [v_name for v_name, v_val in vars if v_val is arg]
            name = e[0]
            kwargs[name] = arg
        except Exception as e:
            message += ': ' + arg
        
    print(message)
    pprint(kwargs)
    return input('')

def makeFileDictResource():
    s = json.dumps(env.dirdict)
    appendVariable(s)

def chooseMultiple(items):
    indexes = rangeFromString(prompt(number(items), 'choose 1 based indexes'))
    return map2(indexes, lambda x: items[x])

#print(chooseMultiple(alist))


#print(isfile(file))


s = '''
00:00:47,292 --> 00:00:49,487
電視機前的觀眾朋友大家好
'''

def getCookUpAStormSubtitles():
    
    def f(x):
        start, end, chinese = x
        data = jieba.cut(chinese, timestamp=[start, end])
        data['timestamp'] = {
            'from': start,
            'to': end,
        }
        promptOnce(data)
        return data

        

    file = glf()
    print(file)
    return 
    s = read(file)
    return print(len(s))
    r = r'(\d+:\d+:\d+).*?(\d+:\d+:\d+).*?\n([\u4e00-\u9fff]+)'
    jieba = Jieba(convert='tw2s')
    data = map2(re.findall(r, s), f)
    outpath = 'cookUpAStorm.jieba.json'
    path = npath('drive', addExtension(outpath, 'json'))
    prompt(path)
    write(path, data)


class ReadParse:
    def __init__(self, x):
        self.text = read(x)
        print(type(self.text))
        prompt()
        
    def run(self, fn, outpath):
        prompt(type(self.text))
        results = fn(self.text)
        path = npath('drive', addExtension(outpath, 'json'))
        dprompt(path)
        write(path, results)
    
def dprompt2(*args):
    import inspect

    store={}
    for arg in args:
        try:
            vars = inspect.currentframe().f_back.f_locals.items()
            name = [v_name for v_name, v_val in vars if v_val is arg][0]
            store[name]=arg
        except Exception as e:
            store[arg] = True
        
    pprint(store)



def stringBreaker(s, key):
    r = '[\w\W]+?' + key + '\s*'
    print(r)
    return re.sub(r, '', s)

def chineseMovieJiebaConverter(file, title, breaker=0):
    assert(isfile(file))
    name = camelCase(title)
    outpath = npath('jsondrive', name + '.jieba.json')
    
    dprompt(name, outpath)
    appleBreaker = 'face into\.\.\.'

    s = read(file)
    jieba = Jieba(convert='tw2s')

    if breaker:
        s = stringBreaker(s, breaker)
    s = linegetter(s)
    def parser(s):
        x = split(s, ',')
        a = x[1]
        b = x[2]
        c = x[-1]
        c = re.sub(notChineseRE, '', c)
        return jieba.cut(c, timestamp=[a,b])

    items = map2(s, parser)
    payload = {
        'title': title,
        'contents': items,
    }
    write(outpath, payload)

#chineseMovieJiebaConverter('/home/kdog3682/TODO/You Are the Apple of My Eye_utf8.ass', 'You Are the Apple of My Eye')

def filesFromString(s, e=''):
    dir, *items = linegetter(s)
    return map2(items, lambda x: npath(dir, addExtension(x, e)))

def doFonts(s):

    examplstr1689969711 = """
    todo
    ZCOOL_KuaiLe
    Zhi_Mang_Xing
    Liu_Jian_Mao_Cao
    Long_Cang
    """

    def fonter(file):
        files = FileState(file).unzip(fontdir)
        prompt(files)
        return files
    
    assert(isdir(fontdir))
    files = filesFromString(s, e='zip')
    allfiles = flat(map2(files, fonter))
    save(allfiles)

def hskPaperTests():
    chdir(trashdir)
    f = FileState(glf())
    files = f.unzip()
    names = map2(files, tail)
    names.sort()
    f = lambda x: toNumber(search('H\d(\d+)\.docx', x))
    transcriptIds = map2(names, f)
    checkpoint = checkpointf(extensions=['ogg', 'mp3'])
    audios = filter(names, checkpoint)

    checkpoint = checkpointf(extensions=['docx'])
    transcripts = filter(names, checkpoint)

    checkpoint = checkpointf(extensions=['pdf'], keepRE='answer', flags=re.I)
    exams = filter(names, checkpoint)

    checkpoint = checkpointf(extensions=['pdf'], keepRE='exam', flags=re.I)
    answers = filter(names, checkpoint)
    def boo(id, items):
        r = str(id)
        return find(items, lambda x: test(r, x))

    def parser(id):
        a = boo(id, audios)
        b = boo(id, exams)
        c = boo(id, answers)
        if not a:
            return 
        if not b:
            return 
        if not c:
            return 

        d = boo(id, transcripts)
        return [a, b, c, d]

    filePacks = map2(transcriptIds, parser)
    prompt(filePacks)

    for filePack in filePacks:
        files = npath(trashdir, filePack)

def toNumber(x):
    try:
        return int(x)
    except Exception as e:
        return 
        
    


#pprint(hskPaperTests()) # renames the files ... and does som stuff


def sortByDate(files, reverse=0):
    files.sort(key=mdate, reverse=reverse)
    return files

#pprint(sortByDate(getFiles('js'), 1))
